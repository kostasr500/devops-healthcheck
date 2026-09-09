variable "location" {
  type        = string
  description = "The Azure region where resources will be deployed"
  default     = "westeurope"
}

variable "environment" {
  type        = string
  description = "Deployment environment name"
  default     = "dev"
}

variable "project_name" {
  type        = string
  description = "Base project name used in resource naming"
  default     = "devops-healthcheck"
}
