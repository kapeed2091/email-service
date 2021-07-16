# Email Service
We use [serverless](https://www.serverless.com/) to deploy code to AWS Lambda

## Install Serverless
There are several ways to install serverless package. 

Refer https://www.serverless.com/framework/docs/getting-started/

Popular way of installing using [NPM](https://www.serverless.com/framework/docs/getting-started#via-npm)

- npm install -g serverless

## Where to make the change
There are potentially two files which needs to be changed
- handler.py
- send_email.py

## Deploy the changes
- serverless deploy -v
- Ensure there are proper AWS credentials configured for deployment to succeed
