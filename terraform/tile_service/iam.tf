/*
 *  IAM Role assumed by API Gateway
 */

# Role
resource "aws_iam_role" "api_gw" {
  name = "${var.name}_api_gw"
  path = "/"
  assume_role_policy = "${data.aws_iam_policy_document.api_gw.json}"

  tags = {
    Name    = "${var.name}_api_gw"
    Project = "${var.project}"
  }
}

# Service using role
data "aws_iam_policy_document" "api_gw" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["apigateway.amazonaws.com"]
    }
  }
}

# In-line policy attachment
resource "aws_iam_role_policy" "api_gw" {
  name = "${var.name}_api_gw"
  role = "${aws_iam_role.api_gw.id}"
  policy = "${data.aws_iam_policy_document.lambda_invoke.json}"
}

# In-line policy definition
data "aws_iam_policy_document" "lambda_invoke" {
  statement {
    sid = "InvokeLambda"
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = ["${module.cog_renderer.lambda_arn}"]
  }
}
