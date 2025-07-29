terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "nc-terraform-state-cicd-demo" # CHANGE THIS!
    key    = "de-etl/terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName   = "CI/CD Demo"
      Team          = "Data Engineering"
      DeployedFrom  = "Terraform"
      Repository    = "deng-cicd"
      CostCentre    = "DE"
      Environment   = "dev"
      RetentionDate = "2025-07-29"
    }
  }
}
