output "RS_STORAGE_ACCOUNT" {
  value = azurerm_storage_account.storage.name
}

output "RS_CONTAINER_NAME" {
  value = azurerm_storage_container.tfstate.name
}

output "RS_RESOURCE_GROUP" {
  value = azurerm_resource_group.rg.name
}
