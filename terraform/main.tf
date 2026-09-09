resource "azurerm_resource_group" "rg" {
  name     = "rg-devops-healthcheck-dev"
  location = "westeurope"

  tags = {
    Environment = "Development"
    Project     = "devops-healthcheck"
    ManagedBy   = "Terraform"
  }
}
