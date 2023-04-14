import boto3
import logging
import time
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']
    service_name = os.getenv('SERVICE_NAME')
    region = os.getenv("MY_AWS_REGION")

    ec2 = boto3.client('ec2', region_name=region)
    all_instances = ec2.describe_instances()
    instance_ids = []

    for reservation in all_instances['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                if instance['State']['Name'] == 'running':
                    print(instance)
                    for tag in instance['Tags']:
                        if tag['Key'] == 'app' and tag['Value'] == service_name:
                            instance_ids.append(instance['InstanceId'])

    if step == "createSecret":
        print(instance_ids)
        change_password = create_secret(arn, token, region)
        change_pass(instance_ids, change_password, region)
    else:
        raise ValueError("Invalid step parameter")

def change_pass(instances, change_password, region):
    ssm_client = boto3.client('ssm', region_name=region)
    # Sending SSM command to change password on instance
    try:
        print('Changing password on Windows instance ' + str(instances))
        response = ssm_client.send_command(InstanceIds=instances,DocumentName='AWS-RunPowerShellScript', Parameters={ 'commands': change_password },)
    except Exception as e:
        print("--------- ERROR ---------")
        print(e)

def create_secret(arn, token, region):
    print('--------- CREATING NEW SECRET ---------')
    secrets_client = boto3.client('secretsmanager', region_name=region)

    # Get previous secret value in case of errors
    previous_password = secrets_client.get_secret_value(SecretId=arn)["SecretString"].split(":")[1].replace('"','').replace('}','').strip()

    try:
        # Generate a random password
        print('--- Generating new password ---')
        password = secrets_client.get_random_password(PasswordLength=32, ExcludeNumbers=False, ExcludePunctuation=True, ExcludeUppercase=False, ExcludeLowercase=False, RequireEachIncludedType=True)["RandomPassword"]
        change_password = [
            "$password = '" + password + "'",
            "$computers = Hostname",
            "net.exe user Administrator $password"
        ]

        # Put the new password
        print('Putting new password into the secret')
        secureString='{ \"Administrator\": \"'+ password +'\"\n }'
        secrets_client.put_secret_value(SecretId=arn,  ClientRequestToken=token, SecretString=secureString, VersionStages=['AWSCURRENT'])
        logger.info("createSecret: Successfully put secret for ARN %s and version %s." % (arn, token))

        time.sleep(10)
        print('--------- NEW SECRET CREATED AND APPLIED TO INSTANCE (COMPLETED) ---------')

        return change_password

    except Exception as e:
        print("--------- ERROR ---------")
        print(e)

        # Restoring old password in case of error
        secureString='{ \"Administrator\": \"'+ previous_password +'\"\n }'
        secrets_client.put_secret_value(SecretId=arn,  SecretString=secureString)
        print("The previous password has been restored in secrets manager")
        return False