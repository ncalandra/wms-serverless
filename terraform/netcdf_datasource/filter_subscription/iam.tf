/*
 *  IAM Role used by this lambda function
 */

# Role
resource "aws_iam_role" "lambda" {
  name = "${var.name}_lambda"
  path = "/"
  assume_role_policy = data.aws_iam_policy_document.lambda.json

  tags = {
    Name    = "${var.name}_lambda"
    Project = var.project
  }
}

# Service using role
data "aws_iam_policy_document" "lambda" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# In-line policy attachment
resource "aws_iam_role_policy" "lambda" {
  name = "${var.name}_lambda"
  role = aws_iam_role.lambda.id
  policy = data.aws_iam_policy_document.lambda_invoke.json
}

# In-line policy definition
data "aws_iam_policy_document" "lambda_invoke" {
  statement {
    sid = "InvokeLambda"
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = [var.processing_function]
  }
}

# AWS CloudWatch policy attachment
resource "aws_iam_role_policy_attachment" "cloudwatch" {
  role       = aws_iam_role.lambda.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
