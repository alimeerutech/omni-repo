#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_ec2,
    aws_lambda,
    aws_kinesis
)

from os import getenv

class LambdaKinesisService2(core.Stack):

    def __init__(self, scope: core.Stack, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Importing a VPC from the "base" platform stack
        self.vpc = aws_ec2.Vpc.from_lookup(self, "PlatformVPC", vpc_name="omni-repo-platform/BaseVPC")
        
        # Lambda function defined here. Using inline code, but realistically would use from_asset as codebase would be much larger :-)
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Code.html#aws_cdk.aws_lambda.Code.from_asset
        self.lambda_function = aws_lambda.Function(
            self, "Service2LambdaFunction",
            code=aws_lambda.Code.inline("def lambda_handler(event, context): return {'message': 'Success'}"),
            handler="index.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            memory_size=128,
            timeout=core.Duration.seconds(6),
            vpc=self.vpc
        )
        
        # Crteating Kinesis Stream for Service 2
        self.kinesis_stream = aws_kinesis.Stream(
            self, "Service2Kinesis",
            shard_count=1,
            retention_period_hours=24
        )
        
        # Granting read/write access to lambda function
        self.kinesis_stream.grant_read_write(self.lambda_function)
    

_env = core.Environment(account=getenv('CDK_DEFAULT_ACCOUNT'), region=getenv('AWS_DEFAULT_REGION'))
app = core.App()
LambdaKinesisService2(app, "lambda-kinesis-service", env=_env)
app.synth()