"""Ingest a new NetCDF File."""

# System Imports
import logging
import os

# External Imports
import boto3
import netcdf_to_geotiff
import stac

# Set environment variables for GDAL and Proj
os.environ["PROJ_LIB"] = "/opt/share/proj"
os.environ["GDAL_DATA"] = "/opt/share/gdal"

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get S3 Client
client = boto3.client("s3")

# Get environment variables
SOURCE_BUCKET = os.environ["source_bucket"]
DEST_BUCKET = os.environ["dest_bucket"]


def handler(event, context):
    """AWS Lambda handler."""
    logger.info(f"Processing File: {event['key']}")

    data = netcdf_to_geotiff.convert(
        SOURCE_BUCKET,
        event["key"],
        event["definition"]["parameter_name"],
        event["definition"]["band"],
        client,
    )

    # Upload to S3
    client.upload_file(data["local_file"], DEST_BUCKET, data["key"])

    # Cleanup
    os.remove(data["local_file"])

    # Write STAC data
    stac.generate(data, DEST_BUCKET, client)
