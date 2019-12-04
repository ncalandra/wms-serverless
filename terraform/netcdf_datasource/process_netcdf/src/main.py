"""Convert NetCDF to a COG."""

# System Imports
import logging
import os
import uuid

# External Imports
import boto3
from osgeo import gdal

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
    input_file = os.path.join("/tmp", "file.nc")

    print(f"Processing File: {event['key']}")

    # Download file
    client.download_file(SOURCE_BUCKET, event["key"], input_file)

    # Convert to GeoTIFF
    temp_file_1 = os.path.join("/tmp", f"{uuid.uuid1()}_1.tif")
    gdal.Translate(
        temp_file_1,
        f"NETCDF:{input_file}:{event['definition']['parameter_name']}",
        format="GTiff",
        bandList=[event["definition"]["band"]],
        outputType=gdal.GDT_Float32,
        creationOptions=["COMPRESS=DEFLATE"],
        unscale=True,  # GDAL warp cannot handle scaled values
    )
    os.remove(input_file)

    # Warp to EPSG:3857
    temp_file_2 = os.path.join("/tmp", f"{uuid.uuid1()}_2.tif")
    gdal.Warp(
        temp_file_2,
        temp_file_1,
        format="GTiff",
        dstSRS="EPSG:3857",
        workingType=gdal.GDT_Float32,
        outputType=gdal.GDT_Float32,
        creationOptions=["COMPRESS=DEFLATE"],
        resampleAlg="cubicspline",
    )
    os.remove(temp_file_1)

    # Apply compression and tiling
    output_file = os.path.join("/tmp", f"{uuid.uuid1()}_final.tif")
    dataset = gdal.Translate(
        output_file,
        temp_file_2,
        format="GTiff",
        creationOptions=["TILED=YES", "COMPRESS=DEFLATE"],
    )
    os.remove(temp_file_2)

    # Add overviews
    dataset.BuildOverviews("NEAREST", [2, 4, 8, 16, 32, 64])

    # Close dataset
    dataset = None

    # Upload to S3
    key = f'{event["key"].split(".")[0]}.tif'
    client.upload_file(output_file, DEST_BUCKET, key)
    os.remove(output_file)
