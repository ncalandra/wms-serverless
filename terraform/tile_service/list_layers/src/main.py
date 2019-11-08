'''List layers in an S3 Bucket.'''
# System Imports
import os
import json

# External Imports
import boto3

SOURCE_BUCKET = os.environ['source_bucket']

# Get S3 Client
client = boto3.client('s3')

def handler(event, context):

    response = client.list_objects_v2(
        Bucket=SOURCE_BUCKET,
        MaxKeys=1000,
    )

    # TODO: add check if there are more than 1000 layers

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps([object['Key'] for object in response['Contents']])
    }
