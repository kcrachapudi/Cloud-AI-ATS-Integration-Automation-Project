import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

JOB_PROFILE = os.getenv('JOB_PROFILE')
# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name= os.getenv('AWS_REGION'))
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))

def fetch_by_job_profile(job_profile):
    """
    Query DynamoDB by job_profile and return a pandas DataFrame
    """
    response = table.query(
        KeyConditionExpression=Key('job_profile').eq(job_profile)
    )

    items = response.get('Items', [])

    if not items:
        print("No data found.")
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(items)

    return df


if __name__ == "__main__":
    df = fetch_by_job_profile(JOB_PROFILE)

    print("\nDataFrame Output:\n")
    print(df)

    # Optional: save to CSV
    df.to_csv("ats_results.csv", index=False)
    print("\nSaved to ats_results.csv")