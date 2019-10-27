/*
 *  The purpose of this module is to define a goes16 datasource
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# Parameters
variable "source_bucket" {}
variable "dest_bucket" {}
variable "parameter" {}

# Lambda functions
module "process_netcdf" {
  source        = "./process_netcdf"
  name          = "${var.name}_process_netcdf"
  project       = "${var.project}"
  role          = "${aws_iam_role.lambda}"
  source_bucket = "${var.source_bucket}"
  dest_bucket   = "${var.dest_bucket}"
  parameter     = "${var.parameter}"
}
