# omni-repo

This repo showcases a monorepo with multiple services built and deployed via cdk.


## Layout

- Platform: This directory builds any baseline dependencies for all of the services (ie, vpc)
- Service_1: Lambda Function with a DynamoDB table. Also granting access from the Function to the table in the code.
- Service_2: Lambda Function with a Kinesis Stream. Also granting access from the Function to the Kinesis stream in the code.
- Service_3: Lambda Function with a Cloudwatch Cron rule. In code, connecting the function to the Cloudwatch rule.
