import os
from aws_cdk import App, Environment
from stacks.s3_web import S3Web

app = App()

S3Web(
    app,
    "S3Web",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION")
    )
)

app.synth()
