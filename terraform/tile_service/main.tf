/*
 *  The purpose of this module is to serve tiles off of S3
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# Parameters
variable "region" {}
variable "source_bucket" {}

# Lambda functions
module "cog_renderer" {
  source        = "./cog_renderer"
  name          = "${var.name}_cog_renderer"
  project       = "${var.project}"
  source_bucket = "${var.source_bucket}"
  api_gateway_arn = "${aws_api_gateway_rest_api.tile.execution_arn}"
}

module "list_layers" {
  source        = "./list_layers"
  name          = "${var.name}_list_layers"
  project       = "${var.project}"
  source_bucket = "${var.source_bucket}"
  api_gateway_arn = "${aws_api_gateway_rest_api.tile.execution_arn}"
}
