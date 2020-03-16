#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_ec2,
    aws_lambda,
    aws_dynamodb
)

from os import getenv

class LambdaService1(core.Stack):

    def __init__(self, scope: core.Stack, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Importing a VPC from the "base" platform stack
        self.vpc = aws_ec2.Vpc.from_lookup(self, "PlatformVPC", vpc_name="omni-repo-platform/BaseVPC")
        
        # Lambda function defined here. Using inline code, but realistically would use from_asset as codebase would be much larger :-)
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Code.html#aws_cdk.aws_lambda.Code.from_asset
        self.lambda_function = aws_lambda.Function(
            self, "LambdaFunction",
            code=aws_lambda.Code.inline("def lambda_handler(event, context): return {'message': 'Success'}"),
            handler="index.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            memory_size=128,
            timeout=core.Duration.seconds(6),
            vpc=self.vpc
        )
    
        # Creating Dynamo Table for Lambda function to use
        self.dynamo_table = aws_dynamodb.Table(
            self, "Service1DynamoTable",
            partition_key=aws_dynamodb.Attribute(name='customer_id', type=aws_dynamodb.AttributeType.STRING),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
        )
        
        # Grant full access of lambda function to DynamoDB Table
        self.dynamo_table.grant_read_write_data(self.lambda_function)


_env = core.Environment(account=getenv('CDK_DEFAULT_ACCOUNT'), region=getenv('AWS_DEFAULT_REGION'))
app = core.App()
LambdaService1(app, "lambda-service-1", env=_env)
app.synth()