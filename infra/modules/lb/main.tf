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

// loadbalancer
resource "ncloud_lb" "main" {
  name = "sns-lb-${var.env}"
  network_type = "PUBLIC"
  type = "NETWORK_PROXY"
  subnet_no_list = [ var.lb_subnet_no ]
}

// target group
resource "ncloud_lb_target_group" "main" {
  vpc_no   = var.vpc_no
  protocol = "PROXY_TCP"
  target_type = "VSVR"
  port        = 8000
  health_check {
    protocol = "TCP"
    http_method = "GET"
    port           = 8000
    url_path       = "/health"
    cycle          = 30
    up_threshold   = 2
    down_threshold = 2
  }
  algorithm_type = "RR"
  name = "sns-tg-${var.env}"
}

resource "ncloud_lb_listener" "lb-listener" {
  load_balancer_no = ncloud_lb.main.load_balancer_no
  protocol = "TCP"
  port = 80
  target_group_no = ncloud_lb_target_group.main.target_group_no
}

// target group attachment
resource "ncloud_lb_target_group_attachment" "main" {
  target_group_no = ncloud_lb_target_group.main.target_group_no
  target_no_list = [var.be_instance_no]
}
