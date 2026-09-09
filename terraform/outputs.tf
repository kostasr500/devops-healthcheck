output "resource_group_name" {
  description = "The name of the provisioned Azure Resource Group"
  value       = azurerm_resource_group.rg.name
}

output "acr_login_server" {
  description = "The URL used to log in and push images to Azure Container Registry"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  description = "The admin username for the Container Registry"
  value       = azurerm_container_registry.acr.admin_username
}
