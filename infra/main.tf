locals {
  tags                       = { azd-env-name : var.environment_name }
  sha                        = base64encode(sha256("${var.environment_name}${var.location}${data.azurerm_client_config.current.subscription_id}"))
  resource_token             = substr(replace(lower(local.sha), "[^A-Za-z0-9_]", ""), 0, 13)
  location                   = var.location
  workspace                  = var.workspace
  is_default_workspace       = local.workspace == "default"
  deploy_observability_tools = var.deploy_observability_tools == "true" && local.workspace == "azure"
}


# ------------------------------------------------------------------------------------------------------
# Deploy resource Group
# ------------------------------------------------------------------------------------------------------
resource "azurecaf_name" "rg_name" {
  name          = var.environment_name
  resource_type = "azurerm_resource_group"
  random_length = 0
  clean_input   = true
}

resource "azurerm_resource_group" "rg" {
  name     = azurecaf_name.rg_name.result
  location = var.location

  tags = local.tags
}
