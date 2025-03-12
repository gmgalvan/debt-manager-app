from aws_cdk import (
    Stack,
    aws_bedrock as bedrock,
    aws_iam as iam
)
from constructs import Construct
from config import CONFIG

class BedrockKnowledgeBasesStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        opensearch_kb = bedrock.CfnKnowledgeBase(self, "KnowledgeBaseOpenSearch",
                                                  knowledge_base_name="MyOpenSearchKnowledgeBase",
                                                  vector_store_config={
                                                      "collection": CONFIG['collection_name'],
                                                      "index": CONFIG['index_name']
                                                  })

        aurora_kb = bedrock.CfnKnowledgeBase(self, "KnowledgeBaseAurora",
                                              knowledge_base_name="MyAuroraKnowledgeBase",
                                              relational_store_config={
                                                  "clusterArn": CONFIG['aurora_cluster_arn'],
                                                  "databaseName": CONFIG['aurora_database_name']
                                              })

        agent = bedrock.CfnAgent(self, "Agent",
                                 agent_name="MyAgent",
                                 # Choose the knowledge base ID you intend to use (for instance, OpenSearch one)
                                 knowledge_base_id=opensearch_kb.ref,
                                 instructions="Provide assistance based on the knowledge base.",
                                 action_groups=["arn:aws:bedrock:action-group/your-action-group-arn"])

        policy = iam.Policy(self, "BedrockPolicy",
                            statements=[
                                iam.PolicyStatement(
                                    actions=["opensearch:*"],
                                    resources=[f"arn:aws:opensearch:{self.region}:{self.account}:collection/{CONFIG['collection_name']}"]
                                ),
                                iam.PolicyStatement(
                                    actions=["rds:*"],
                                    resources=[CONFIG['aurora_cluster_arn']]
                                )
                            ])
        agent_role = iam.Role(self, "AgentRole",
                              assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"))
        policy.attach_to_role(agent_role)
