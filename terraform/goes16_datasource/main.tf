/*
 *  The purpose of this module is to define a goes16 datasource
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# Parameters
variable "source_bucket" {}
variable "dest_bucket" {}

# Lambda functions
module "filter_subscription" {
  source  = "./filter_subscription"
  name    = "${var.name}_filter_subscription"
  project = "${var.project}"
}

module "process_netcdf" {
  source        = "./process_netcdf"
  name          = "${var.name}_process_netcdf"
  project       = "${var.project}"
  source_bucket = "${var.source_bucket}"
  dest_bucket   = "${var.dest_bucket}"
}
