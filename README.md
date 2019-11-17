# WMS Serverless

A Serverless implementation of WMS on AWS.

This repository contains a [terraform](https://www.terraform.io/) project that implements a serverless version of [WMS](https://www.opengeospatial.org/standards/wms) on [AWS](https://aws.amazon.com/).

A live demo can be found here: https://nathancalandra.cloud/goes16-serverless

## Components

This project consists of three modules.

### S3

This modules contains the main S3 bucket used in this project.  It's purpose is store layers that will be served by the API.  The data source module can be used to automatically add files to this bucket.  To prevent storing large amounts of data, a life-cycle policy is applied to delete any object older than one day.

### NetCDF Data Source

This module contains lambda functions and an SNS subscription that are used to convert NetCDF files on the `noaa-goes16` public S3 bucket to [COGs](https://www.cogeo.org/).  It can be configured to pull as much data as desired from the source bucket.  It's default configuration pulls a single product.  To add more products edit the `data_definitions` variable in `terraform/main.tf`.  For example, the following configuration processes bands 2 and 9 from the Cloud Moisture Imagery (CMI) product.  See the [documentation](https://docs.opendata.aws/noaa-goes16/cics-readme.html) on the public goes16 S3 bucket for a description of the available data.

```hcl
[{
  filter_regex   = "ABI-L2-CMIPF\\/[0-9]{4}\\/[0-9]{3}/[0-9]{2}/OR_ABI-L2-CMIPF-M6C09.*.nc"
  parameter_name = "CMI"
  band           = 1
}, {
  filter_regex   = "ABI-L2-CMIPF\\/[0-9]{4}\\/[0-9]{3}/[0-9]{2}/OR_ABI-L2-CMIPF-M6C02.*.nc"
  parameter_name = "CMI"
  band           = 1
}]
```

### WMS API

The WMS API module uses API Gateway and lambda functions to operate on files stored in the S3 bucket.  Currently there are two endpoints:

#### wms

This is endpoint supports a partial implementation of the WMS "GetMap" request.

#### layers

This endpoint simply lists layers in the main S3 bucket.  It is a placeholder until WMS "GetCapabilities" is supported.

## Installation

1. Install [terraform](https://www.terraform.io/downloads.html)
1. Open a terminal inside the terraform directory
1. Run `terraform init`
1. Provide variables for s3 backend storage
1. Run `terraform apply`

## AWS Services used by this project

- [S3](https://aws.amazon.com/s3/)
- [Lambda](https://aws.amazon.com/lambda/)
- [SNS](https://aws.amazon.com/sns/)
- [API Gateway](https://aws.amazon.com/api-gateway/)


## Lambda, GDAL, and Python

https://github.com/developmentseed/geolambda
