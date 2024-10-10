# child_module/outputs.tf

output "vpc_ids" {
  description = "VPC IDs from root module"
  value       = module.vpc_module.vpc_ids
}

output "subnet_ids" {
  description = "Subnet IDs from root module"
  value       = module.vpc_module.subnet_ids
}
