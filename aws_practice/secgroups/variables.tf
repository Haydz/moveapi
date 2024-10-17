variable "sg_name" {
  type = string

}

variable "sg_description" {
  type    = string
  default = "no description given"

}

variable "ingress_ports" {
  type = list(number)

}

variable "outgress_rules" {
  type = list(object({
    cidr_ipv4 = string
    from_port = number
    to_port   = number

  }))

}


# variable "security_groups" {
#     description = "a map of secrity groupd with rules"
#     type = map(object({
#         name = string
#         description = string
#         ingress_ports = list(number)
#         outgress_rules = list(object( {
#             cidr_ipv4 = string
#             from_port = number
#             to_port = number
#         }))
#     }))
# }