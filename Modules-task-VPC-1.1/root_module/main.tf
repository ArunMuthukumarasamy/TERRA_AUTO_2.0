module "vpc" {
  source = "../root_module"

  vpc_cidr_block = var.vpc_cidr_block
  azs            = var.azs
  public_subnets = var.public_subnets
  private_subnets = var.private_subnets
  region         = var.region
}
