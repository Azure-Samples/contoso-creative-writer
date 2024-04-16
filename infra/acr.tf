resource "azurecaf_name" "acr_name" {
  count         = local.is_default_workspace ? 0 : 1
  name          = local.resource_token
  resource_type = "azurerm_container_registry"
  random_length = 0
  clean_input   = true
}

resource "azurerm_container_registry" "acr" {
  count               = local.is_default_workspace ? 0 : 1
  name                = azurecaf_name.acr_name[0].result
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Premium"
  admin_enabled       = false
  tags                = azurerm_resource_group.rg.tags
}
