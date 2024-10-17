// going to use this for a module
// but need to choose default VPC
// and an instance

data "aws_vpc" "main" {
  provider = aws.sec
  id       = "vpc-0bac1bc6c50fa5939"
}

# resource "aws_security_group" "example" {
#   provider    = aws.sec
#   name        = "example"
#   description = "example"
#   vpc_id      = data.aws_vpc.main.id
#   tags = {
#     Name = "example"
#   }
# }


module "security_groups" {
  source         = "./secgroups"
  sg_name        = "sg1"
  sg_description = "this is a description"
  ingress_ports  = [80, 443]
  outgress_rules = [
    {
      cidr_ipv4 = "10.0.0.8/32"
      from_port = 443
      to_port   = 443
    }
  ]
}

module "security_groups2" {
  source         = "./secgroups"
  sg_name        = "sg2"
  sg_description = "this is a description"
  ingress_ports  = [80, 443]
  outgress_rules = [
    {
      cidr_ipv4 = "10.0.0.8/32"
      from_port = 443
      to_port   = 443
    }
  ]
}

# output "secgroup_output" {
#   value = module.security_groups.secgroup_name_id
# }

# module "security_groups" {
#   source = "./secgroups"

#   # Pass the map of security groups with their respective rules
#   security_groups = {
#     sg1 = {
#       name           = "sg1"
#       description    = "Security group 1"
#       ingress_ports  = [80,443]
#       outgress_rules = []
#     },
#     sg2 = {
#       name           = "sg2"
#       description    = "Security group 2"
#       ingress_ports  = [80]
#       outgress_rules = [
#         {
#           cidr_ipv4 = "0.0.0.0/0"
#           from_port = 443
#           to_port   = 443
#         },
#         {
#           cidr_ipv4 = "0.0.0.0/0"
#           from_port = 80
#           to_port   = 80
#         }
#       ]
#     }
#   }
# }

# Output the names and IDs of the security groups created by the child module
output "security_group_names" {
  value = module.security_groups.secgroup_name_id
}


locals {
    toppings = ["lettuce","tomatoes","jalapenos","onions"]
}

resource "local_file" "for_each_loop" {
    for_each = toset(local.toppings)
    content     = "${each.value}"
    filename = "${path.module}/${each.value}.foreach"
}

output "try" {
    value = local_file.for_each_loop["onions"].filename
}


resource "aws_instance" "by_set" {
  for_each = toset(var.instance_set)
  provider = aws.sec
  ami = "ami-0b08bfc6ff7069aff"
  instance_type = "t2.micro"

  tags = {
    Name = each.value
  }
}

output "instance_name" {
    value = aws_instance.by_set["Instance A"].public_ip
}

resource "aws_instance" "by_map" {
      provider = aws.sec
    for_each = var.instance_map
      ami = "ami-0b08bfc6ff7069aff"
  instance_type = "t2.micro"
  
  tags = {
    Name = each.value
    ID = each.key
  }
}

output "instance_map_name" {
    
    value = aws_instance.by_map["inst_a"].ami
}