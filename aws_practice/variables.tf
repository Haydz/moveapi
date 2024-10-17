variable "instance_set" {
  type = list(string)
  default = ["Instance A", "Instance B"]
}


variable "instance_map" {
  type = map(string)
  default = {
    "inst_a" = "Instance A",
    "inst_b" = "Instance B"
  }
}