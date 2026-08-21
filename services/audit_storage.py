import boto3
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

def store_report_to_s3(report_data: dict) -> dict:
    bucket = os.getenv("AWS_S3_BUCKET")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "ap-south-1")

    if not bucket or not access_key:
        return {"stored": False, "reason": "AWS credentials or bucket not configured"}

    try:
        s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        key = f"clientshield-reports/{report_data['id']}.json"
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(report_data, default=str), ContentType="application/json")
        return {"stored": True, "key": key}
    except Exception as e:
        return {"stored": False, "reason": str(e)}