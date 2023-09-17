output "be_ip" {
  value = ncloud_public_ip.be.public_ip
}

output "db_ip" {
  value = ncloud_public_ip.db.public_ip
}

output "lb_domain" {
  value = module.loadBalancer.lb-domain
}
