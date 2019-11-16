/*
 *  Lambda function filters an SNS subscription
 */

# Name and Project Tags
variable "name" {type = string}
variable "project" {type = string}

# Parameters
variable "sns_topic_arn" {type = string}
variable "processing_function" {type = string}
variable "compile_patterns" {type = list(string)}

# Archive Source Code
data "archive_file" "filter_subscription" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/src.zip"
}

resource "aws_lambda_function" "filter_subscription" {
  filename         = "${path.module}/src.zip"
  source_code_hash = "${data.archive_file.filter_subscription.output_base64sha256}"
  function_name    = "${var.name}"
  description      = "Filter the sns topic"
  role             = "${aws_iam_role.lambda.arn}"
  handler          = "main.handler"
  runtime          = "python3.7"
  timeout          = 120

  environment {
    variables = {
      processing_function = "${var.processing_function}"
      compile_patterns    = "${jsonencode(var.compile_patterns)}"
    }
  }

  tags = {
    Name    = "${var.name}"
    Project = "${var.project}"
  }
}

# Allow SNS to invoke this lambda function
resource "aws_lambda_permission" "allow_SNS" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.filter_subscription.function_name}"
  principal     = "sns.amazonaws.com"
  source_arn    = "${var.sns_topic_arn}"
}

# Return Lambda ARN
output "lambda_arn" {
  value = "${aws_lambda_function.filter_subscription.arn}"
}
