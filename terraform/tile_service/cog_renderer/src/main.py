'''Convert a COG to png.'''
# System Imports
import base64
import os

# External Imports
from osgeo import gdal, osr

SOURCE_BUCKET = os.environ['source_bucket']

# Set environment variables for GDAL and Proj
os.environ['PROJ_LIB'] = '/opt/share/proj'
os.environ['GDAL_DATA'] = '/opt/share/gdal'

def handler(event, context):

    layername = event['queryStringParameters']['LAYERS']
    width = event['queryStringParameters']['WIDTH']
    height = event['queryStringParameters']['HEIGHT']
    bounding_box = event['queryStringParameters']['BBOX'].split(',')

    # Convert to GeoTIFF
    gdal.Translate(
        os.path.join('/tmp', 'file.png'),
        f'/vsis3/{SOURCE_BUCKET}/{layername}',
        outputType=gdal.GDT_Byte,
        width=width,
        height=height,
        projWin=[bounding_box[0], bounding_box[3], bounding_box[2], bounding_box[1]],
        projWinSRS='EPSG:3857',
        scaleParams=[]
    )

    with open(os.path.join('/tmp', 'file.png'), 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return {
        'isBase64Encoded': True,
        'statusCode': 200,
        'headers': {'Content-Type': 'image/png'},
        'body': encoded_image
    }
