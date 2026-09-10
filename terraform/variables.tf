variable "location" {
  type        = string
  description = "The Azure region where resources will be deployed"
  default     = "italynorth"
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

variable "target_url" {
  type        = string
  description = "The target URL for the health check container to test"
  default     = "https://httpbin.org/status/200"
}
