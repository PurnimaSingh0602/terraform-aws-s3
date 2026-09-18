terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "iac_bucket" {
  bucket = "purnima-iac-demo-2026"

  tags = {
    Name        = "IaC Demo Bucket"
    Environment = "Lab"
  }
}

resource "aws_s3_bucket_public_access_block" "iac_bucket" {
  bucket = aws_s3_bucket.iac_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "iac_bucket" {
  bucket = aws_s3_bucket.iac_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "iac_bucket" {
  bucket = aws_s3_bucket.iac_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_ownership_controls" "iac_bucket" {
  bucket = aws_s3_bucket.iac_bucket.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}
