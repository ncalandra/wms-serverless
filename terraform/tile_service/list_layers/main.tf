/*
 *  Lambda function that lists available layers
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# Parameters
variable "source_bucket" {}
variable "api_gateway_arn" {}

# Archive Source Code
data "archive_file" "list_layers" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/src.zip"
}

resource "aws_lambda_function" "list_layers" {
  filename         = "${path.module}/src.zip"
  source_code_hash = "${data.archive_file.list_layers.output_base64sha256}"

  function_name    = "${var.name}"
  description      = "Lists layers in an S3 Bucket"
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
  function_name = "${aws_lambda_function.list_layers.function_name}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_arn}/*/GET/layers"
}

# Return Lambda ARN
output "lambda_arn" {
  value = "${aws_lambda_function.list_layers.arn}"
}
