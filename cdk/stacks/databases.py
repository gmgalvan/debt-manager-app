from aws_cdk import (
    App,
    Stack,
    RemovalPolicy,
    Duration,
)
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from aws_cdk import aws_opensearchserverless as opensearch
from constructs import Construct

class DataBasesStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Use the default VPC available in your account
        default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # Provision an Aurora Serverless Cluster (Aurora MySQL)
        aurora_cluster = rds.ServerlessCluster(
            self, "AuroraServerlessCluster",
            engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
            vpc=default_vpc,
            scaling=rds.ServerlessScalingOptions(
                auto_pause=Duration.minutes(10),
                min_capacity=rds.AuroraCapacityUnit.ACU_2,
                max_capacity=rds.AuroraCapacityUnit.ACU_8,
            ),
            default_database_name="KnowledgeBaseDB",
            removal_policy=RemovalPolicy.DESTROY  # For production, consider using RETAIN
        )

        # Provision an OpenSearch Serverless Collection (VECTORSEARCH type)
        opensearch_collection = opensearch.CfnCollection(
            self, "OpenSearchCollection",
            name="knowledgebase-collection",
            type="VECTORSEARCH"
        )