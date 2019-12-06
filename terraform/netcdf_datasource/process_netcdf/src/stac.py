"""Convert NetCDF to a geoTIFF."""

# System Imports
import json
import logging

# External Imports
import boto3

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get S3 Client
client = boto3.client("dynamodb")


def generate(data, bucket, s3_client):
    """
    Generate Required STAC files and upload to S3.

    Args:
        data: information about the new data that was written to S3
        bucket: S3 bucket
        s3_client: boto3 S3 client

    """
    generate_item(data, bucket, s3_client)
    generate_item_db(data)


def generate_item(data, bucket, s3_client):
    """
    Generate a STAC item and upload to S3.

    Args:
        data: information about the new data that was written to S3
        bucket: S3 bucket
        s3_client: boto3 S3 client

    """
    stac_item = {
        "type": "Feature",
        "id": data["key"].split(".")[0],
        "bbox": data["bbox"],
        "geometry": "shapely",
        "properties": {"datetime": ""},
        "assets": {
            f"B{data['band']}": {
                "type": "image/x.geotiff",
                "eo:bands": [9],
                "title": "Some title?",
                "href": data["key"],
            }
        },
        "links": [
            {"rel": "self", "href": f"./{data['key'].split('.')[0]}.json"},
            {"rel": "parent", "href": "../catalog.json"},
            {"rel": "root", "href": "../../../../../catalog.json"},
        ],
    }
    s3_client.put_object(
        Body=json.dumps(stac_item),
        Bucket=bucket,
        Key=f"{data['key'].split('.')[0]}.json",
    )


def generate_item_db(data):
    """
    Generate a STAC item and upload to dynamodb.

    Args:
        data: information about the new data that was written to S3

    """
    item_id = (
        "/".join(data["key"].split("/")[0:4])
        + data["key"].split("/")[-1].split("_")[4][1:-3]
    )
    client.put_item(
        TableName="wms_serverless_data_catalog",
        Item={
            "catalog": {"S": "NOAA-GOES-16"},
            "id": {"S": item_id},
            "assets": {
                "M": {
                    f"B{data['band']}": {
                        "M": {
                            "type": {"S": "image/x.geotiff"},
                            "title": {"S": "Some title?"},
                            "href": {"S": data["key"]},
                        }
                    }
                }
            },
            "links": {
                "L": [
                    {"M": {"rel": {"S": "self"}, "href": {"S": "self.json"}}},
                    {"M": {"rel": {"S": "parent"}, "href": {"S": "parent.json"}}},
                    {"M": {"rel": {"S": "root"}, "href": {"S": "root.json"}}},
                ]
            },
        },
    )
