resource "azurerm_monitor_workspace" "example" {
  count               = local.deploy_observability_tools ? 1 : 0
  name                = "amon-${local.resource_token}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

resource "azurerm_log_analytics_workspace" "example" {
  count               = local.deploy_observability_tools ? 1 : 0
  name                = "alog-${local.resource_token}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_data_collection_rule" "example_msci" {
  count               = local.deploy_observability_tools ? 1 : 0
  name                = "msci-${azurerm_resource_group.rg.location}-${azurerm_kubernetes_cluster.aks[0].name}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  kind                = "Linux"

  data_sources {
    extension {
      name           = "ContainerInsightsExtension"
      extension_name = "ContainerInsights"
      streams        = ["Microsoft-ContainerInsights-Group-Default"]
      extension_json = <<JSON
      {
        "dataCollectionSettings": {
          "interval": "1m",
          "namespaceFilteringMode": "Off",
          "enableContainerLogV2": true
        }
      }
      JSON
    }
  }

  destinations {
    log_analytics {
      workspace_resource_id = azurerm_log_analytics_workspace.example[0].id
      name                  = azurerm_log_analytics_workspace.example[0].name
    }
  }

  data_flow {
    streams      = ["Microsoft-ContainerInsights-Group-Default"]
    destinations = [azurerm_log_analytics_workspace.example[0].name]
  }
}

resource "azurerm_monitor_data_collection_rule_association" "example_msci_to_aks" {
  count                   = local.deploy_observability_tools ? 1 : 0
  name                    = "msci-${azurerm_kubernetes_cluster.aks[0].name}"
  target_resource_id      = azurerm_kubernetes_cluster.aks[0].id
  data_collection_rule_id = azurerm_monitor_data_collection_rule.example_msci[0].id
}


resource "azurerm_application_insights" "applicationinsights" {
  count               = local.deploy_observability_tools ? 1 : 0
  name                = "ai-${local.resource_token}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.example[0].id
  tags                = local.tags
}
