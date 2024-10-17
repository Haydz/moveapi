
# // good for 1 security group

//added map variable for multiple
resource "aws_security_group" "sec_module" {
  provider    = aws.sec
  name        = var.sg_name
  description = var.sg_description
  vpc_id      = "vpc-0bac1bc6c50fa5939"
  tags = {
    Name = var.sg_name
  }
}


// going to make it so you can add multiple rules
resource "aws_vpc_security_group_ingress_rule" "sec_module" {
  provider          = aws.sec
  count             = length(var.ingress_ports)
  security_group_id = aws_security_group.sec_module.id

  cidr_ipv4   = "10.0.0.0/8"
  from_port   = var.ingress_ports[count.index]
  ip_protocol = "tcp"
  to_port     = var.ingress_ports[count.index]
}

resource "aws_vpc_security_group_egress_rule" "sec_module" {
  provider          = aws.sec
  count             = length(var.outgress_rules)
  security_group_id = aws_security_group.sec_module.id

  cidr_ipv4   = var.outgress_rules[count.index].cidr_ipv4
  from_port   = var.outgress_rules[count.index].from_port
  ip_protocol = "tcp"
  to_port     = var.outgress_rules[count.index].to_port
}


output "secgroup_name_id" {
    
  value = aws_security_group.sec_module.name
}



# resource "aws_vpc_security_group_ingress_rule" "sec_module" {
#   provider          = aws.sec
#   count             = length(var.ingress_ports)
#   security_group_id = aws_security_group.sec_module.id

#   cidr_ipv4   = "10.0.0.0/8"
#   from_port   = var.ingress_ports[count.index]
#   ip_protocol = "tcp"
#   to_port     = var.ingress_ports[count.index]
# }

# resource "aws_vpc_security_group_ingress_rule" "sec_module" {
#   provider          = aws.sec
#   for_each = { for sg_name, sg_info in var.security_groups : sg_name => sg_info.ingress_ports }
#   security_group_id = aws_security_group.sec_module[each.key].id

#   cidr_ipv4   = "10.0.0.0/8"
#   from_port   = each.value[count.index]
#   ip_protocol = "tcp"
#   to_port     = each.value[count.index]
# }

# # Create egress rules for each security group
# resource "aws_vpc_security_group_egress_rule" "sec_module" {
#   provider          = aws.sec
#   for_each          = { for sg_name, sg_info in var.security_groups : sg_name => sg_info.outgress_rules }

#   count             = length(each.value) # Number of egress rules
#   security_group_id = aws_security_group.sec_module[each.key].id
#   cidr_ipv4         = each.value[count.index].cidr_ipv4
#   from_port         = each.value[count.index].from_port
#   to_port           = each.value[count.index].to_port
#   ip_protocol       = "tcp"
# }
# Output the security group names
# output "secgroup_name_id" {
#   value = { for sg_name, sg_info in aws_security_group.sec_module : sg_name => sg_info.name }
# }

