"""Convert NetCDF to a COG."""

# System Imports
import logging
import os

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
    output_file = os.path.join("/tmp", "file.tif")

    print(f"Processing File: {event['key']}")

    # Download file
    client.download_file(SOURCE_BUCKET, event["key"], input_file)

    # Convert to GeoTIFF
    dataset = gdal.Translate(
        "",
        f"NETCDF:{input_file}:{event['definition']['parameter_name']}",
        format="MEM",
        bandList=[event["definition"]["band"]],
        outputType=gdal.GDT_Float32,
        unscale=True,  # GDAL warp cannot handle scaled values
    )

    # Warp to EPSG:3857
    dataset = gdal.Warp(
        "",
        dataset,
        format="MEM",
        dstSRS="EPSG:3857",
        workingType=gdal.GDT_Float32,
        outputType=gdal.GDT_Float32,
        resampleAlg="cubicspline",
    )

    # Apply compression and tiling
    dataset = gdal.Translate(
        output_file,
        dataset,
        format="GTiff",
        creationOptions=["TILED=YES", "COMPRESS=DEFLATE"],
    )

    # Add overviews
    dataset.BuildOverviews("NEAREST", [2, 4, 8, 16, 32, 64])

    # Close dataset
    dataset = None

    # Upload to S3
    key = f'{event["key"].split(".")[0]}.tif'
    client.upload_file(output_file, DEST_BUCKET, key)
