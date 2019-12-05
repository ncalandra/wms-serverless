/*
 *  The purpose of this module is to manage all S3 resources
 */

# Name and Project Tags
variable "name" {}
variable "project" {}

# S3 Bucket Name
variable "s3_bucket_name" {}

# Main S3 bucket
resource "aws_s3_bucket" "data" {
  bucket = var.s3_bucket_name
  acl = "private"
  tags = {
    Name = var.name
    Project = var.project
  }

  # Apply default encryption for all objects
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  # Expire items older than 1 day
  lifecycle_rule {
    id      = "expire"
    enabled = true

    expiration {
      days = 1
    }
  }
}

# block all public access
resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
