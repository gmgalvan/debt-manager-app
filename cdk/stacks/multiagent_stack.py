from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
)
from aws_cdk.aws_bedrock import CfnAgent, CfnAgentAlias
from constructs import Construct

class MultiAgentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # -------------------------------
        # Collaborator Agent 1: Debt Advice
        # -------------------------------
        collaborator1 = CfnAgent(
            self,
            "CollaboratorAgent1",
            agent_name="DebtAdviceAgent",
            agent_resource_role_arn="arn:aws:iam::123456789012:role/DebtAdviceAgentRole",
            foundation_model="anthropic.claude-v2",  # example model
            instruction="You provide advice on debt management.",
        )
        collaborator1_alias = CfnAgentAlias(
            self,
            "CollaboratorAgent1Alias",
            agent_alias_name="debt-advice-alias",
            agent=collaborator1.ref,
            description="Alias for the Debt Advice Agent",
        )

        # -------------------------------
        # Collaborator Agent 2: Investment Advice
        # -------------------------------
        collaborator2 = CfnAgent(
            self,
            "CollaboratorAgent2",
            agent_name="InvestmentAdviceAgent",
            agent_resource_role_arn="arn:aws:iam::123456789012:role/InvestmentAdviceAgentRole",
            foundation_model="anthropic.claude-v2",  # example model
            instruction="You provide advice on investment opportunities.",
        )
        collaborator2_alias = CfnAgentAlias(
            self,
            "CollaboratorAgent2Alias",
            agent_alias_name="investment-advice-alias",
            agent=collaborator2.ref,
            description="Alias for the Investment Advice Agent",
        )

        # -------------------------------
        # Supervisor Agent: Query Router
        # -------------------------------
        supervisor_agent = CfnAgent(
            self,
            "SupervisorAgent",
            agent_name="SupervisorAgent",
            agent_resource_role_arn="arn:aws:iam::123456789012:role/SupervisorAgentRole",
            foundation_model="anthropic.claude-v2",  # example model
            instruction=(
                "You are a supervisor agent. Based on the user query, forward debt-related queries "
                "to the DebtAdviceAgent and investment-related queries to the InvestmentAdviceAgent."
            ),
            # Configure collaborators (agent_collaborators is a list of dictionaries)
            agent_collaborators=[
                {
                    "agentDescriptor": {
                        "aliasArn": collaborator1_alias.attr_agent_alias_arn
                    },
                    "collaborationInstruction": "Forward debt-related queries.",
                    "collaboratorName": "DebtAdviceAgent"
                },
                {
                    "agentDescriptor": {
                        "aliasArn": collaborator2_alias.attr_agent_alias_arn
                    },
                    "collaborationInstruction": "Forward investment-related queries.",
                    "collaboratorName": "InvestmentAdviceAgent"
                }
            ]
        )
        supervisor_alias = CfnAgentAlias(
            self,
            "SupervisorAgentAlias",
            agent_alias_name="supervisor-alias",
            agent=supervisor_agent.ref,
            description="Alias for the Supervisor Agent",
        )

        # -------------------------------
        # Outputs
        # -------------------------------
        CfnOutput(self, "SupervisorAgentId", value=supervisor_agent.ref)
        CfnOutput(self, "DebtAdviceAgentId", value=collaborator1.ref)
        CfnOutput(self, "InvestmentAdviceAgentId", value=collaborator2.ref)
