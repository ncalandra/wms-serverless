"""Convert a COG to png."""
# System Imports
import base64
import logging
import os

# External Imports
from osgeo import gdal

# Set environment variables for GDAL and Proj
os.environ["PROJ_LIB"] = "/opt/share/proj"
os.environ["GDAL_DATA"] = "/opt/share/gdal"

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get environment variables
SOURCE_BUCKET = os.environ["source_bucket"]


def handler(event, context):
    """AWS Lambda handler."""
    layername = event["queryStringParameters"]["LAYERS"]
    width = event["queryStringParameters"]["WIDTH"]
    height = event["queryStringParameters"]["HEIGHT"]
    bounding_box = event["queryStringParameters"]["BBOX"].split(",")
    style = event["queryStringParameters"]["STYLES"]

    # Convert to GeoTIFF
    gdal_raster = gdal.Translate(
        "",
        f"/vsis3/{SOURCE_BUCKET}/{layername}",
        format="MEM",
        width=width,
        height=height,
        projWin=[bounding_box[0], bounding_box[3], bounding_box[2], bounding_box[1]],
        projWinSRS="EPSG:3857",
        scaleParams=[],
    )

    # Add color
    gdal.DEMProcessing(
        os.path.join("/tmp", "file.png"),
        gdal_raster,
        "color-relief",
        addAlpha=True,
        colorFilename=os.path.join("styles", f"{style}.csv"),
    )
    gdal_raster = None

    with open(os.path.join("/tmp", "file.png"), "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/png",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,access-control-allow-origin",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": encoded_image,
    }
