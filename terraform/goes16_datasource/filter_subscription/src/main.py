'''Parse SNS event notification.'''
# System Imports
import json
import os
import re

# External Imports
import boto3

PROCESSING_FUNCTION = os.environ['processing_function']

# Get Lambda Client
client = boto3.client('lambda')

def handler(event, context):

    sns_record = event['Records'][0]['Sns']

    # Pull the fine name
    goes16_event = json.loads(sns_record['Message'])
    file_name = goes16_event['Records'][0]['s3']['object']['key']
    print(file_name)

    file_pattern = re.compile(r'ABI-L2-CMIPF\/[0-9]{4}\/[0-9]{3}/[0-9]{2}/OR_ABI-L2-CMIPF-M6C09.*.nc')
    if file_pattern.fullmatch(file_name):
        print('Processing')
        client = boto3.client('lambda')
        client.invoke(
            FunctionName=PROCESSING_FUNCTION,
            InvocationType='Event',
            Payload=json.dumps({
                'key': file_name
            })
        )

    return
