#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_ec2
)


class PlatformStack(core.Stack):

    def __init__(self, scope: core.Stack, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create tags to be applied to VPC
        #self.tags = core.Tag(
        #    self, "VPCTags",
        #)

        # This resource alone will create a private/public subnet in each AZ as well as nat/internet gateway(s)
        self.vpc = aws_ec2.Vpc(
            self, "BaseVPC",
            cidr='10.0.0.0/24',
        )
        

app = core.App()
PlatformStack(app, "omni-repo-platform")
app.synth()