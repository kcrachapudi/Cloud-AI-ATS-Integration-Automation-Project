import json
import boto3
import os
from decimal import Decimal
from dotenv import load_dotenv

# Read from .env for local testing
load_dotenv()

#Load AWS credentials from environment variables for local testing
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')    
DEFAULT_OUTPUT_FORMAT = os.getenv('DEFAULT_OUTPUT_FORMAT')  
AWS_MODEL_INFERENCE_PROFILE = os.getenv('AWS_MODEL_INFERENCE_PROFILE')
JOB_PROFILE = os.getenv('JOB_PROFILE')
DYNAMO_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')    

# AWS Clients
s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

# DynamoDB Table
table = dynamodb.Table(DYNAMO_TABLE_NAME)

# Hardcoded job profile (can be dynamic later)
job_profile = "aiml-engineer"

def lambda_handler(event, context):
    # 1️⃣ Get S3 details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Processing file: {key}")

    #Read file (local OR S3)
    try:
        # Local testing
        with open(key, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        # S3 mode
        #file_obj = s3.get_object(Bucket=bucket, Key=key)
        #text = file_obj['Body'].read().decode('utf-8', errors='ignore')
        print("File Not Found.")
        return 
    #Create AI prompt
    prompt = f"""
You are an ATS system.

Job Profile:
{JOB_PROFILE}

Job Description:
Looking for Python, AWS, DevOps, AI/ML experience.

Resume:
{text[:2000]}

Return ONLY valid JSON:
{{
  "score": number,
  "skills_matched": [],
  "skills_missing": [],
  "recommendation": ""
}}
"""

    #Call Bedrock (Inference Profile REQUIRED)
    response = bedrock.invoke_model(
        modelId= AWS_MODEL_INFERENCE_PROFILE,
        body=json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 300,
                "temperature": 0.3
            }
        })
    )

    #Parse AI response
    response_body = json.loads(response['body'].read())
    result_text = response_body['output']['message']['content'][0]['text']

    print("AI RESULT:", result_text)

    #Convert to JSON safely
    try:
        result_json = json.loads(result_text)
    except:
        print("Invalid JSON from AI")
        result_json = {}

    #Store in DynamoDB
    score_decimal = Decimal(str(result_json.get("score", 0))) # DynamoDB needs Decimal for numbers does not support float
    table.put_item(
        Item={
            "job_profile": job_profile,   # 🔑 Partition Key
            "resume_id": key,             # 🔑 Sort Key
            "score": score_decimal,
            "skills_matched": result_json.get("skills_matched", []),
            "skills_missing": result_json.get("skills_missing", []),
            "recommendation": result_json.get("recommendation", ""),
            "raw_output": result_text
        }
    )

    print("Saved to DynamoDB")

    return {
        "statusCode": 200,
        "body": result_text
    }


#LOCAL TESTING SUPPORT
if __name__ == "__main__":
    with open("test_event.json") as f:
        event = json.load(f)

    lambda_handler(event, None)    