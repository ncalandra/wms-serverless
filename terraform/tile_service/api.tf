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
