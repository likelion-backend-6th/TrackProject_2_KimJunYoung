terraform {
  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }
  }
  required_version = ">= 0.13"
}

// Configure the ncloud provider
provider "ncloud" {
  access_key = var.NCP_ACCESS_KEY
  secret_key = var.NCP_SECRET_KEY
  region = "KR"
  site = "PUBLIC"
  support_vpc = true
}

locals {
  env = "staging"
}

module "network" {
  source = "../modules/network"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  env = local.env
}
