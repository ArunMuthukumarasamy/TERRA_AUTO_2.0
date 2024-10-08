provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "imported_vpc" {
  # The block remains empty for now since we're importing
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID to import"
  type        = string
}
