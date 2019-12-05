resource "aws_sns_topic_subscription" "new_goes_object" {
  topic_arn = var.sns_topic_arn
  protocol  = "lambda"
  endpoint  = module.filter_subscription.lambda_arn
}
