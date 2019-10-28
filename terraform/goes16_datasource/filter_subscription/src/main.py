'''Parse SNS event notification.'''
import json

def handler(event, context):

    sns_record = event['Records'][0]['Sns']

    # Pull the fine name
    goes16_event = json.loads(sns_record['Message'])
    file_name = goes16_event['Records'][0]['s3']['object']['key']
    print(file_name)
