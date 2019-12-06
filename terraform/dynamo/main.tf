/*
 *  The purpose of this module is to define a dynamodb table used to the data catalog
 */

# Name and Project Tags
variable "name" {}
variable "project" {}


resource "aws_dynamodb_table" "data_catalog" {
  name           = "${var.name}_data_catalog"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "catalog"
  range_key      = "id"

  attribute {
    name = "catalog"
    type = "S"
  }

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name        = "${var.name}_data_catalog"
    Environment = var.project
  }
}

# Return table arn
output "table" {
  value = aws_dynamodb_table.data_catalog.arn
}
