import json

# Optionally try to import aws_bedrock as bedrock; if unavailable, use boto3.
try:
    import aws_bedrock as bedrock
except ImportError:
    import boto3
    bedrock = None

def lambda_handler(event, context):
    print("Orchestrator received event:", event)
    
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("prompt", "")
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON", "message": str(e)})
        }
    
    import os
    debt_function = os.environ.get("DEBT_AGENT_FUNCTION")
    investment_function = os.environ.get("INVESTMENT_AGENT_FUNCTION")
    
    # Prepare payload for agent Lambdas.
    payload = json.dumps({"prompt": prompt})
    
    lambda_client = boto3.client("lambda")
    
    # Invoke Debt Agent Lambda.
    try:
        debt_resp = lambda_client.invoke(
            FunctionName=debt_function,
            InvocationType="RequestResponse",
            Payload=payload
        )
        debt_result = json.loads(debt_resp["Payload"].read().decode("utf-8"))
    except Exception as e:
        debt_result = {"error": str(e)}
    
    # Invoke Investment Agent Lambda.
    try:
        invest_resp = lambda_client.invoke(
            FunctionName=investment_function,
            InvocationType="RequestResponse",
            Payload=payload
        )
        invest_result = json.loads(invest_resp["Payload"].read().decode("utf-8"))
    except Exception as e:
        invest_result = {"error": str(e)}
    
    combined = {
        "debt_advice": debt_result.get("response", debt_result),
        "investment_advice": invest_result.get("response", invest_result)
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps({"combined_response": combined})
    }
