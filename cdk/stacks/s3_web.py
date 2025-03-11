import os
from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3deploy

class S3Web(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        website_bucket = s3.Bucket(
            self, 
            "WebsiteBucket",
            bucket_name="gm-galvan-debt-manager-webapp",  # Must be globally unique
            website_index_document="index.html",
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS
        )

        # Compute the absolute path to the "build" folder in your React/Vue/Angular/etc. app.
        asset_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../frontend/build")
        )
        print("Deploying asset from:", asset_path)

        # Deploy the static files from the build folder into the S3 bucket
        s3deploy.BucketDeployment(
            self, 
            "DeployWebsite",
            sources=[s3deploy.Source.asset(asset_path)],
            destination_bucket=website_bucket,
        )

        # Output the website's S3 endpoint URL
        CfnOutput(self, "WebsiteURL", value=website_bucket.bucket_website_url)
