# Tiling API

resource "aws_api_gateway_rest_api" "tile" {
  name        = "${var.name}"
  body        = "${data.template_file.openapi.rendered}"
}

# Open API definition
data "template_file" "openapi" {
  template = "${file("${path.module}/api.yaml")}"

  vars = {
    name         = "${var.name}"
    cog_renderer = "${module.cog_renderer.lambda_arn}"
    region       = "${var.region}"
    credentials  = "${aws_iam_role.api_gw.arn}"
  }
}

# API Deployment
resource "aws_api_gateway_deployment" "demo" {
  rest_api_id       = "${aws_api_gateway_rest_api.tile.id}"
  stage_name        = "demo"

  # Set the description to a hash of the OpenAPI file to force updates on changes
  stage_description = "${md5(file("${path.module}/api.yaml"))}"
}
