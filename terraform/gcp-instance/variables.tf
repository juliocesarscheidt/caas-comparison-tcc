variable "project_id" {
  type        = string
  description = "Project ID"
}

variable "region" {
  type        = string
  description = "Project Region"
  default     = "southamerica-east1"
}

variable "zone" {
  type        = string
  description = "Project Zone"
  default     = "southamerica-east1-a"
}

variable "instance_type" {
  type        = string
  default     = "f1-micro"
  description = "Instance Type"
}

variable "instance_image" {
  type        = string
  default     = "debian-cloud/debian-10"
  description = "Instance Image"
}

variable "instance_username" {
  type        = string
  default     = "google"
  description = "Instance Username"
}
