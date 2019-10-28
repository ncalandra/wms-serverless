resource "aws_sns_topic_subscription" "new_goes_object" {
  topic_arn = "arn:aws:sns:us-east-1:123901341784:NewGOES16Object"
  protocol  = "lambda"
  endpoint  = "${module.filter_subscription.lambda_arn}"
}
