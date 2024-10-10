
# variable "aws_region" {
#   description = "The AWS region where resources will be managed."
#   type        = string
# }
variable "aws_region" {
  description = "The AWS region where resources will be managed."
  type        = string
}

variable "vpc_configs" {
  description = "List of VPC configurations."
  type = list(object({
    vpc_id            = string
    cidr_block        = string
    tags              = map(string)
    subnet_configs    = list(object({
      subnet_id         = string
      cidr_block        = string
      availability_zone = string
      tags              = map(string)
    }))
  }))
}
