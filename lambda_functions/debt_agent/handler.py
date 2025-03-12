import json

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("prompt", "")
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON", "message": str(e)})}
    
    # Create a combined prompt.
    system_prompt = "You are a debt advice agent. Provide actionable suggestions to manage and reduce debt."
    full_prompt = f"{system_prompt}\nUser: {prompt}\nAgent:"
    
    # Simulate a response (replace with Bedrock Converse API call if desired).
    response_text = "Consider consolidating your debts and seeking professional financial counseling."
    
    return {
        "statusCode": 200,
        "body": json.dumps({"agent": "debt", "response": response_text})
    }
