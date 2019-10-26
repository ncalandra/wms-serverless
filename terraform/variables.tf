# AWS Credentials
variable "access_key" {
  type        = string
  description = "AWS Access Key"
}
variable "secret_key" {
  type        = string
  description = "AWS Secret Key"
}
variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "us-east-1"
}

# Name and Project Tags
variable "name" {
  type        = "string"
  description = "Name prefix used by all resources"
}
variable "project" {
  type        = "string"
  description = "A 'project' tag is added to all resources to track cost"
}

# Main S3 Bucket name
variable "s3_bucket_name" {
  type        = "string"
  description = "Name for the S3 bucket where data is stored.  S3 bucket names must be unique"
}
