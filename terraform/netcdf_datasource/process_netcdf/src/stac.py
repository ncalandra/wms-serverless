"""Convert NetCDF to a geoTIFF."""

# System Imports
import json
import logging

# External Imports

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def generate(data, bucket, s3_client):
    """
    Generate Required STAC files and upload to S3.

    Args:
        data: information about the new data that was written to S3
        bucket: S3 bucket
        s3_client: boto3 S3 client

    """
    generate_item(data, bucket, s3_client)


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
