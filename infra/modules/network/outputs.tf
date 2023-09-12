output "vpc_no" {
  value = ncloud_vpc.vpc.vpc_no
}

output "main_subnet_no" {
  value = ncloud_subnet.main.subnet_no
}

output "lb_subnet_no" {
  value = ncloud_subnet.lb.subnet_no
}
