provider "aws" {
  region = var.region
}

# Create  new custome arun_VPC1 and arun_VPC2
module "vpc" {
  source     = "../Root-module"
  for_each   = { for k, v in var.vpcs : k => v if k != "arun_VPC" }
  cidr_block = each.value.cidr_block
  vpc_name   = each.key
}

# VPC to Import.
resource "aws_vpc" "default_vpc" {
  for_each = { arun_VPC = var.vpcs["arun_VPC"] }

  cidr_block = each.value.cidr_block

  tags = {
    Name = "arun_VPC"
  }
}

