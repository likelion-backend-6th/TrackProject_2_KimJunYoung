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
  env = "prod"
}

module "network" {
  source = "../modules/network"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  env = local.env
}

module "be_server" {
  source = "../modules/server"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  env = local.env
  name = "be"
  product_code = data.ncloud_server_products.sm.product_code
  server_image_product_code = data.ncloud_server_products.sm.server_image_product_code
  vpc_no = module.network.vpc_no
  subnet_no = module.network.main_subnet_no
  acg_port_range = 8000
  init_script_path = "be_init_script.tftpl"
  init_script_envs = {
    DB_HOST = ncloud_public_ip.db.public_ip
    password = var.password
    POSTGRES_DB = var.POSTGRES_DB
    POSTGRES_USER = var.POSTGRES_USER
    POSTGRES_PASSWORD = var.POSTGRES_PASSWORD
    POSTGRES_PORT = var.POSTGRES_PORT
    DJANGO_SETTINGS_MODULE = var.DJANGO_SETTINGS_MODULE
    DJANGO_SECRET_KEY = var.DJANGO_SECRET_KEY
    NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
    NCP_SECRET_KEY = var.NCP_SECRET_KEY
  }

}

module "db_server" {
  source = "../modules/server"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  env = local.env
  name = "db"
  product_code = data.ncloud_server_products.sm.product_code
  server_image_product_code = data.ncloud_server_products.sm.server_image_product_code
  vpc_no = module.network.vpc_no
  subnet_no = module.network.main_subnet_no
  acg_port_range = 5432
  init_script_path = "db_init_script.tftpl"
  init_script_envs = {
    password = var.password
    POSTGRES_DB = var.POSTGRES_DB
    POSTGRES_USER = var.POSTGRES_USER
    POSTGRES_PASSWORD = var.POSTGRES_PASSWORD
    POSTGRES_PORT = var.POSTGRES_PORT
  }
}

module "loadBalancer" {
  source = "../modules/lb"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  env = local.env
  lb_subnet_no = module.network.lb_subnet_no
  vpc_no = module.network.vpc_no
  be_instance_no = module.be_server.instance_no
}

resource "ncloud_public_ip" "be" {
    server_instance_no = module.be_server.instance_no
}

resource "ncloud_public_ip" "db" {
    server_instance_no = module.db_server.instance_no
}

data "ncloud_server_products" "sm" {
  server_image_product_code = "SW.VSVR.OS.LNX64.UBNTU.SVR2004.B050"
  product_code = "SVR.VSVR.HICPU.C002.M004.NET.SSD.B050.G002"
}
