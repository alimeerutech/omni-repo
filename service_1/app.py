#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_dynamodb
)


class DynamodbStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create dynamo table
        demo_table = aws_dynamodb.Table(
            self, "demo_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

app = core.App()
DynamodbStack(app, "DynamodbStack")
app.synth()