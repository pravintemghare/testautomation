### Step to deploy CodePipeline in single account for infrastrucuture automation.

## Setup Git2S3 

1. Deploy Git2S3 cfn template using the following command.
``aws cloudformation deploy --template-file .\automation\git2s3.yml --stack-name git2s3-deploy-cfn --parameter-overrides "file://C:\Users\pravi\OneDrive\Desktop\testautomation\automation\config\git2s3.json" --capabilities CAPABILITY_NAMED_IAM``
2. Configure WebHook in the respective repository. (Details for webhook available in output of the Git2S3 Stack & secretid provided in parameters.)
3. Add SSH key to the repository. (Details for SSH key available in output of the Git2S3 stack)

## Deploy CloudFormation deploy role
1: For first time deployment provide fake parameters for ArtifactBucketArn & ArtifactKey As we haven't created them yet. They will be created in pipeline cfn template. We need to re-run the same command to update bucket & key with correct values.
2: Deploy role cfn template using the following command.
``aws cloudformation deploy --template-file .\automation\cloudformation-deploy-role.yaml --stack-name cloudformation-automation-role --parameter-overrides "file://C:\Users\pravi\OneDrive\Desktop\testautomation\automation\config\cloudformation-deploy-role.json" --capabilities CAPABILITY_NAMED_IAM``
## Deploy Pipeline

1. Deploy pipeline cfn template using the following command.
``aws cloudformation deploy --template-file .\automation\pipeline.yaml --stack-name codepipeline-deploy-cfn --parameter-overrides "file://C:\Users\pravi\OneDrive\Desktop\testautomation\automation\config\pipeline.json" --capabilities CAPABILITY_NAMED_IAM``

## Update the CloudFormation deploy role with correct values
1. Deploy role cfn template using the following command.
``aws cloudformation deploy --template-file .\automation\cloudformation-deploy-role.yaml --stack-name cloudformation-automation-role --parameter-overrides "file://C:\Users\pravi\OneDrive\Desktop\testautomation\automation\config\cloudformation-deploy-role.json" --capabilities CAPABILITY_NAMED_IAM``
