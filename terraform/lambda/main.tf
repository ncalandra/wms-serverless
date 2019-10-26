/*
 *  The purpose of this module is to manage all Lambda resources
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# Functions
module "process_netcdf" {
  source  = "./process_netcdf"
  name    = "${var.name}_process_netcdf"
  project = "${var.project}"
  role    = "${aws_iam_role.lambda}"
}
