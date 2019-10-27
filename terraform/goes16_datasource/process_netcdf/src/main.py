import os
import boto3
from osgeo import gdal, osr

fname = "ABI-L2-CMIPF/2019/299/20/OR_ABI-L2-CMIPF-M6C16_G16_s20192992030373_e20192992040092_c20192992040171.nc"

SOURCE_BUCKET = os.environ['source_bucket']
DEST_BUCKET = os.environ['dest_bucket']
PARAMETER = os.environ['parameter']

def handler(event, context):

    input_file = os.path.join('/tmp', 'file.nc')
    output_file = os.path.join('/tmp', 'file.tif')

    client = boto3.client('s3')
    client.download_file(SOURCE_BUCKET, fname, input_file)

    # Open dataset
    gdal_raster = gdal.Translate(
        '',
        f'NETCDF:{input_file}:{PARAMETER}',
        format='MEM',
        bandList=[1]
    )

    # Convert to EPSG:3857
    # srs = osr.SpatialReference(wkt=gdal_raster.GetProjection())
    # srs_string = srs.GetAttrValue('AUTHORITY', 0) + ':' + srs.GetAttrValue('AUTHORITY', 1)
    # print(f'Source SRS: {srs_string}')

    # gdal_raster = gdal.Warp(
    #     '',
    #     gdal_raster,
    #     format='MEM',
    #     srcSRS=srs_string,
    #     dstSRS='EPSG:3857'
    # )

    # Write to disk
    gdal_raster = gdal.Translate(
        output_file,
        gdal_raster,
        format='GTiff'
    )
    print(os.listdir('/tmp'))

    # Upload to S3
    client.upload_file(output_file, DEST_BUCKET, 'ABI-L2-CMIPF/test.tif')
