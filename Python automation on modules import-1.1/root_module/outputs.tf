# root_module/outputs.tf

output "vpc_ids" {
  description = "IDs of the VPCs"
  value       = [for vpc in aws_vpc.vpcs : vpc.id]
}

output "subnet_ids" {
  description = "IDs of the Subnets"
  value       = [for subnet in aws_subnet.subnets : subnet.id]
}
