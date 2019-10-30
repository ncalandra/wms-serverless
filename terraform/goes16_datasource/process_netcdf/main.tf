/*
 *  Lambda function that converts a NetCDF file to a COG
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# Parameters
variable "source_bucket" {}
variable "dest_bucket" {}

# Archive Source Code
data "archive_file" "process_netcdf" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/src.zip"
}

resource "aws_lambda_function" "process_netcdf" {
  filename         = "${path.module}/src.zip"
  source_code_hash = "${data.archive_file.process_netcdf.output_base64sha256}"
  layers           = [
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda-python:3",
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda:4"
  ]
  function_name    = "${var.name}"
  role             = "${aws_iam_role.lambda.arn}"
  handler          = "main.handler"
  runtime          = "python3.7"
  timeout          = 300
  memory_size      = 512

  environment {
    variables = {
      source_bucket = "${var.source_bucket}"
      dest_bucket   = "${var.dest_bucket}"
    }
  }

  tags = {
    Name    = "${var.name}"
    Project = "${var.project}"
  }
}

# Return Lambda ARN
output "lambda_arn" {
  value = "${aws_lambda_function.process_netcdf.arn}"
}
