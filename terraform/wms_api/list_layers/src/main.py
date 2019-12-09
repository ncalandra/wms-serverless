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
    layers = list_bucket(SOURCE_BUCKET, "", continuation_token=None, objects=None)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,access-control-allow-origin",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(layers),
    }


def list_bucket(bucket, prefix, continuation_token=None, objects=None):
    """
    Recursively lists contents on an S3 bucket.

    Args:
        bucket: S3 Bucket Name
        prefix: Prefix to use for objects
        continuation_token: used for pagination
        objects: running list of objects
    Returns:
        list of objects in the bucket with the specified prefix

    """
    if objects is None:
        objects = []

    if not continuation_token:
        response = client.list_objects_v2(Bucket=bucket, MaxKeys=1000, Prefix=prefix)
    else:
        response = client.list_objects_v2(
            Bucket=bucket,
            MaxKeys=1000,
            Prefix=prefix,
            ContinuationToken=continuation_token,
        )

    if "Contents" in response:
        objects.extend(
            [
                s3_object["Key"]
                for s3_object in response["Contents"]
                if ".tif" in s3_object["Key"]
            ]
        )

    if "NextContinuationToken" in response:
        return list_bucket(
            bucket,
            prefix,
            continuation_token=response["NextContinuationToken"],
            objects=objects,
        )

    return objects
