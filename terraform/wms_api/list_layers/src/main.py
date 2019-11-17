"""List layers in an S3 Bucket."""
# System Imports
import json
import logging
import os

# External Imports
import boto3

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get environment variables
SOURCE_BUCKET = os.environ["source_bucket"]

# Get S3 Client
client = boto3.client("s3")


def handler(event, context):
    """AWS Lambda handler."""
    # TODO: add check if there are more than 1000 layers
    response = client.list_objects_v2(Bucket=SOURCE_BUCKET, MaxKeys=1000,)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,access-control-allow-origin",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps([s3_object["Key"] for s3_object in response["Contents"]]),
    }
