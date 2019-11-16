/*
 *  The purpose of this module is to define a goes16 datasource
 */

# Name and Project Tags
variable "name" {type = string}
variable "project" {type = string}

# Parameters
variable "sns_topic_arn" {
  type = string
  default = "arn:aws:sns:us-east-1:123901341784:NewGOES16Object"
}
variable "source_bucket" {
  type = string
  default = "noaa-goes16"
}
variable "dest_bucket" {type = string}
variable "data_definitions" {
  type    = list(object({
    filter_regex   = string
    parameter_name = string
    band           = number
  }))
  default = [
    {
      filter_regex   = "ABI-L2-CMIPF\\/[0-9]{4}\\/[0-9]{3}/[0-9]{2}/OR_ABI-L2-CMIPF-M6C09.*.nc"
      parameter_name = "CMI"
      band           = 1
    }
  ]
}

# Lambda functions
module "filter_subscription" {
  source              = "./filter_subscription"
  name                = "${var.name}_filter_subscription"
  project             = "${var.project}"
  sns_topic_arn       = "${var.sns_topic_arn}"
  processing_function = "${module.process_netcdf.lambda_arn}"
  compile_patterns    = "${var.data_definitions[*].filter_regex}"
}

module "process_netcdf" {
  source              = "./process_netcdf"
  name                = "${var.name}_process_netcdf"
  project             = "${var.project}"
  source_bucket       = "${var.source_bucket}"
  dest_bucket         = "${var.dest_bucket}"
  data_definitions    = "${var.data_definitions}"
}
