"""Parse SNS event notification."""

# System Imports
import json
import logging
import os
import re

# External Imports
import boto3

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get environment variables
PROCESSING_FUNCTION = os.environ["processing_function"]
DATA_DEFINITIONS = json.loads(os.environ["data_definitions"])

# Get Lambda Client
client = boto3.client("lambda")


def handler(event, context):
    """AWS Lambda handler."""
    sns_record = event["Records"][0]["Sns"]

    # Pull the fine name
    goes16_event = json.loads(sns_record["Message"])
    file_name = goes16_event["Records"][0]["s3"]["object"]["key"]
    logger.info(file_name)

    for definition in DATA_DEFINITIONS:
        file_pattern = re.compile(definition["filter_regex"])
        if file_pattern.fullmatch(file_name):
            logger.info(f"Processing: {file_name}")
            client = boto3.client("lambda")
            client.invoke(
                FunctionName=PROCESSING_FUNCTION,
                InvocationType="Event",
                Payload=json.dumps({"key": file_name, "definition": definition}),
            )

    return
