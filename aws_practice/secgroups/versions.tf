terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  alias   = "sec"
  region  = "us-east-1"
  profile = "009160028333_AdministratorAccess"
}

//pretend using S3 backend

