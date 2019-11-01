/*
 *  Lambda function that converts a COG to an image
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# Parameters
variable "source_bucket" {}
variable "api_gateway_arn" {}

# Archive Source Code
data "archive_file" "cog_renderer" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/src.zip"
}

resource "aws_lambda_function" "cog_renderer" {
  filename         = "${path.module}/src.zip"
  source_code_hash = "${data.archive_file.cog_renderer.output_base64sha256}"
  layers           = [
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda-python:3",
    "arn:aws:lambda:us-east-1:552188055668:layer:geolambda:4"
  ]
  function_name    = "${var.name}"
  description      = "Convert a COG to an image"
  role             = "${aws_iam_role.lambda.arn}"
  handler          = "main.handler"
  runtime          = "python3.7"
  timeout          = 300
  memory_size      = 128

  environment {
    variables = {
      source_bucket = "${var.source_bucket}"
    }
  }

  tags = {
    Name    = "${var.name}"
    Project = "${var.project}"
  }
}

# Allow API Gateway to invoke this lambda function
resource "aws_lambda_permission" "allow_API_GW" {
  statement_id  = "AllowExecutionFromAPIGW"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cog_renderer.function_name}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_arn}"
}

# Return Lambda ARN
output "lambda_arn" {
  value = "${aws_lambda_function.cog_renderer.arn}"
}
