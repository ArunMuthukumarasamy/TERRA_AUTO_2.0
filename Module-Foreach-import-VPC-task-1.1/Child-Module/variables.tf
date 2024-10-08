variable "region" {
  description = "AWS region"
  type        = string
}

variable "vpcs" {
  description = "Map of VPCs to create or import"
  type = map(object({
    cidr_block = string
  }))
}
