# Specify the provider and access details
provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region = "${var.aws_region}"
}

# Configure terraform to store its state on S3
terraform {
  backend "s3" {}
}

# Modules
module "geos16" {
  source           = "./netcdf_datasource"
  name             = "${var.name}_goes16"
  project          = "${var.project}"
  sns_topic_arn    = "arn:aws:sns:us-east-1:123901341784:NewGOES16Object"
  source_bucket    = "noaa-goes16"
  dest_bucket      = "${var.s3_bucket_name}"
  data_definitions = [{
    filter_regex   = "ABI-L2-CMIPF\\/[0-9]{4}\\/[0-9]{3}/[0-9]{2}/OR_ABI-L2-CMIPF-M6C09.*.nc"
    parameter_name = "CMI"
    band           = 1
  }, {
    filter_regex   = "ABI-L2-CMIPC\\/[0-9]{4}\\/[0-9]{3}/[0-9]{2}/OR_ABI-L2-CMIPC-M6C09.*.nc"
    parameter_name = "CMI"
    band           = 1
  }]
}

module "s3" {
  source         = "./s3"
  name           = "${var.name}"
  project        = "${var.project}"
  s3_bucket_name = "${var.s3_bucket_name}"
}

module "wms_api" {
  source        = "./wms_api"
  name          = "${var.name}"
  project       = "${var.project}"
  source_bucket = "${var.s3_bucket_name}"
  region        = "${var.aws_region}"
}
