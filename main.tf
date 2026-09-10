terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
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
