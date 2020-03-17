from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    core,
)


class LambdaCronStack(core.Stack):
    
    def __init__(self, scope: core.Stack, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_function = lambda_.Function(
            self, "Service2LambdaFunction",
            code=lambda_.Code.inline("def lambda_handler(event, context): return {'message': 'Success'}"),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_7,
            memory_size=128,
            timeout=core.Duration.seconds(6),
        )

        # Run every day at 6PM UTC
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        self.rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )
        
        self.rule.add_target(targets.LambdaFunction(self.lambda_function))


app = core.App()
LambdaCronStack(app, "LambdaCronExample")
app.synth()
