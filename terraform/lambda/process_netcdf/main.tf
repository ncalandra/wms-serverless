/*
 *  Lambda function that converts a NetCDF file to a COG
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# IAM role
variable "role" {}

# Archive Source Code
data "archive_file" "process_netcdf" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/src.zip"
}

resource "aws_lambda_function" "source" {
  filename         = "${path.module}/src.zip"
  source_code_hash = "${data.archive_file.process_netcdf.output_base64sha256}"
  layers           = [
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda-python:3",
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda:4"
  ]
  function_name    = "${var.name}"
  role             = "${var.role.arn}"
  handler          = "main.handler"
  runtime          = "python3.7"
  timeout          = 120
}
