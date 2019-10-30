'''Convert NetCDF to a COG.'''
# System Imports
import os

# External Imports
import boto3
from osgeo import gdal, osr

SOURCE_BUCKET = os.environ['source_bucket']
DEST_BUCKET = os.environ['dest_bucket']

def handler(event, context):

    input_file = os.path.join('/tmp', 'file.nc')
    output_file = os.path.join('/tmp', 'file.tif')

    client = boto3.client('s3')
    client.download_file(SOURCE_BUCKET, event['key'], input_file)

    gdal.Translate(
        output_file,
        f'NETCDF:{input_file}:CMI',
        format='GTiff',
        bandList=[1],
        #creationOptions=['TILED=YES', 'COPY_SRC_OVERVIEWS=YES', 'COMPRESS=DEFLATE']
    )

    # Upload to S3
    key = f'{event["key"].split(".")[0]}.tif'
    client.upload_file(output_file, DEST_BUCKET, key)


# def process_in_mem():
#     # Open dataset
#     gdal_raster = gdal.Translate(
#         '',
#         f'NETCDF:{input_file}:CMI',
#         format='MEM',
#         bandList=[1]
#     )
#
#     # Convert to EPSG:3857
#     srs = osr.SpatialReference(wkt=gdal_raster.GetProjection())
#     srs_string = srs.GetAttrValue('AUTHORITY', 0) + ':' + srs.GetAttrValue('AUTHORITY', 1)
#     print(f'Source SRS: {srs_string}')
#
#     gdal_raster = gdal.Warp(
#         '',
#         gdal_raster,
#         format='MEM',
#         srcSRS=srs_string,
#         dstSRS='EPSG:3857'
#     )
#
#     # Write to disk
#     gdal_raster = gdal.Translate(
#         output_file,
#         gdal_raster,
#         format='GTiff'
#     )
