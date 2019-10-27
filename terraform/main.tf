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
module "ABI_L2_CMIPF" {
  source        = "./goes16_datasource"
  name          = "${var.name}"
  project       = "${var.project}"
  source_bucket = "noaa-goes16"
  dest_bucket   = "${var.s3_bucket_name}"
  parameter     = "CMI"
}

module "s3" {
  source         = "./s3"
  name           = "${var.name}"
  project        = "${var.project}"
  s3_bucket_name = "${var.s3_bucket_name}"
}
