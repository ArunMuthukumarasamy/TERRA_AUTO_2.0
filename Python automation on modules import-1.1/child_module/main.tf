# child_module/main.tf

terraform {
  backend "local" {
    path = "../Python automation on modules import-1.1/child_module/.terraform/terraform.tfstate"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Adjust the version as needed
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc_module" {
  source      = "../root_module"
  aws_region  = var.aws_region  # Pass aws_region to the module
  vpc_configs = var.vpc_configs
}
