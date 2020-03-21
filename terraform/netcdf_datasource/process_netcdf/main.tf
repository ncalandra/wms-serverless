/*
 *  Lambda function that converts a NetCDF file to a COG
 */

# Name and Project Tags
variable "name" {type = string}
variable "project" {type = string}

# Parameters
variable "source_bucket" {type = string}
variable "dest_bucket" {type = string}

# Archive Source Code
data "archive_file" "process_netcdf" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/src.zip"
}

resource "aws_lambda_function" "process_netcdf" {
  filename         = "${path.module}/src.zip"
  source_code_hash = data.archive_file.process_netcdf.output_base64sha256
  layers           = [
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda-python:3",
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda:4"
  ]
  function_name    = var.name
  description      = "Convert a NetCDF file to a COG"
  role             = aws_iam_role.lambda.arn
  handler          = "main.handler"
  runtime          = "python3.7"
  timeout          = 900
  memory_size      = 384

  environment {
    variables = {
      source_bucket = var.source_bucket
      dest_bucket   = var.dest_bucket
    }
  }

  tags = {
    Name    = var.name
    Project = var.project
  }
}

# Return Lambda ARN
output "lambda_arn" {
  value = aws_lambda_function.process_netcdf.arn
}
