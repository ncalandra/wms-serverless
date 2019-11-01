'''Convert a COG to png.'''
# System Imports
import os

# External Imports
import boto3
from osgeo import gdal, osr

SOURCE_BUCKET = os.environ['source_bucket']

# Set environment variables for GDAL and Proj
os.environ['PROJ_LIB'] = '/opt/share/proj'
os.environ['GDAL_DATA'] = '/opt/share/gdal'

def handler(event, context):
    print('hello world')
