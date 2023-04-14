### Step to deploy CodePipeline in single account for infrastrucuture automation.

## Setup Git2S3 

1. Deploy Git2S3 cfn template using the following command.
``aws cloudformation deploy --template-file .\automation\git2s3.yml --stack-name git2s3-deploy-cfn --parameter-overrides "file://C:\Users\pravi\OneDrive\Desktop\testautomation\automation\config\git2s3.json" --capabilities CAPABILITY_NAMED_IAM``
2. Configure WebHook in the respective repository. (Details for webhook available in output of the Git2S3 Stack & secretid provided in parameters.)
3. Add SSH key to the repository. (Details for SSH key available in output of the Git2S3 stack)

## Deploy Pipeline

1. Deploy pipeline cfn template using the following command.
2.
