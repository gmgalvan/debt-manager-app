import json

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("prompt", "")
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON", "message": str(e)})}
    
    system_prompt = "You are an investment advice agent. Provide insights on investments and portfolio diversification."
    full_prompt = f"{system_prompt}\nUser: {prompt}\nAgent:"
    
    response_text = "Consider diversifying your portfolio with low-cost index funds and bonds."
    
    return {
        "statusCode": 200,
        "body": json.dumps({"agent": "investment", "response": response_text})
    }
