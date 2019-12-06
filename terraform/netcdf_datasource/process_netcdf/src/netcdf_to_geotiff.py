"""Convert NetCDF to a geoTIFF."""

# System Imports
import logging
import os
import uuid

# External Imports
from osgeo import gdal

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def convert(netcdf_bucket, netcdf_key, parameter_name, band, s3_client):
    """
    Convert a NetCDF File to a Cloud Optimzed GeoTIFF (COG).

    Args:
        netcdf_bucket: Name of the NetCDF source S3 Bucket
        netcdf_key: Key to the NetCDF File
        parameter_name: Name of the NetCDF Parameter to extract
        band: Band number to extract
        s3_client: Boto3 S3 client

    Returns:
        data: Object containing information about the new COG

    """
    input_file = os.path.join("/tmp", "file.nc")

    # Download file
    s3_client.download_file(netcdf_bucket, netcdf_key, input_file)

    # Convert to GeoTIFF
    temp_file_1 = os.path.join("/tmp", f"{uuid.uuid1()}_1.tif")
    gdal.Translate(
        temp_file_1,
        f"NETCDF:{input_file}:{parameter_name}",
        format="GTiff",
        bandList=[band],
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

    return {
        "local_file": output_file,
        "key": f'{netcdf_key.split(".")[0]}.tif',
        "bbox": [0, 0, 0, 0],
        "band": band,
    }
