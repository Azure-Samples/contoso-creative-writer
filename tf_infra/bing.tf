resource "azurecaf_name" "bing_name" {
  name          = "bing-${local.resource_token}"
  resource_type = "azurerm_cognitive_account"
  random_length = 4
  clean_input   = true
}

resource "azapi_resource" "bing" {
  type                      = "Microsoft.Bing/accounts@2020-06-10"
  schema_validation_enabled = false
  name                      = azurecaf_name.bing_name.result
  parent_id                 = azurerm_resource_group.rg.id
  location                  = "global"
  body = jsonencode({
    sku = {
      name = "S1"
    }
    kind = "Bing.Search.v7" # or "Bing.CustomSearch"
  })
  response_export_values = ["*"]
}

# get the bing search api access keys
data "azapi_resource_action" "bing" {
  type                   = "Microsoft.Bing/accounts@2020-06-10"
  resource_id            = azapi_resource.bing.id
  action                 = "listKeys"
  method                 = "POST"
  response_export_values = ["*"]
}