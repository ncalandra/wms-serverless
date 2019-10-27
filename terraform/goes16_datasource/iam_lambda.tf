/*
 *  IAM Roles used by lambda
 */


resource "aws_iam_role" "lambda" {
  name = "${var.name}_lambda"
  path = "/"
  assume_role_policy = "${data.aws_iam_policy_document.lambda.json}"

  tags = {
    Name    = "${var.name}"
    Project = "${var.project}"
  }
}

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

resource "aws_iam_role_policy" "s3" {
  name = "${var.name}_s3"
  role = "${aws_iam_role.lambda.id}"
  policy = "${data.aws_iam_policy_document.s3.json}"
}

data "aws_iam_policy_document" "s3" {
  statement {
    sid = "S3ListBucket"
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = ["arn:aws:s3:::${var.source_bucket}"]
  }

  statement {
    sid = "S3GetObject"
    effect = "Allow"
    actions = [
      "s3:GetObject"
    ]
    resources = ["arn:aws:s3:::${var.source_bucket}/*"]
  }

  statement {
    sid = "S3PutObject"
    effect = "Allow"
    actions = [
      "s3:PutObject"
    ]
    resources = ["arn:aws:s3:::${var.dest_bucket}/*"]
  }
}
