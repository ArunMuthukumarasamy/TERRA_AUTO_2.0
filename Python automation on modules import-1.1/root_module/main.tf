# root_module/main.tf

provider "aws" {
  region = var.aws_region
}

# Create VPCs
resource "aws_vpc" "vpcs" {
  for_each = { for vpc in var.vpc_configs : vpc.vpc_id => vpc }

  cidr_block = each.value.cidr_block
  tags       = each.value.tags
}

# Flatten subnets
locals {
  all_subnets = flatten([
    for vpc in var.vpc_configs : [
      for subnet in vpc.subnet_configs : {
        vpc_id            = vpc.vpc_id
        subnet_id         = subnet.subnet_id
        cidr_block        = subnet.cidr_block
        availability_zone = subnet.availability_zone
        tags              = subnet.tags
      }
    ]
  ])
}

# Create Subnets
resource "aws_subnet" "subnets" {
  for_each = { for subnet in local.all_subnets : subnet.subnet_id => subnet }

  vpc_id            = aws_vpc.vpcs[each.value.vpc_id].id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.availability_zone
  tags              = each.value.tags
}
