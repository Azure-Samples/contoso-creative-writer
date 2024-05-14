resource "azurecaf_name" "search_name" {
  name          = local.resource_token
  resource_type = "azurerm_search_service"
  random_length = 0
  clean_input   = true
}

resource "azurerm_search_service" "search" {
  name                = azurecaf_name.search_name.result
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku                 = "basic"

  local_authentication_enabled = true
  authentication_failure_mode  = "http403"
  semantic_search_sku = "free"
}