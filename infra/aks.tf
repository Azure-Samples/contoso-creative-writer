resource "azurecaf_name" "aks_name" {
  count         = local.is_default_workspace ? 0 : 1
  name          = local.resource_token
  resource_type = "azurerm_kubernetes_cluster"
  random_length = 0
  clean_input   = true
}

resource "azurerm_kubernetes_cluster" "aks" {
  count               = local.is_default_workspace ? 0 : 1
  name                = azurecaf_name.aks_name[0].result
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = azurecaf_name.aks_name[0].result
  tags                = azurerm_resource_group.rg.tags

  default_node_pool {
    name       = "system"
    vm_size    = "Standard_D4s_v4"
    node_count = 3
  }

  identity {
    type = "SystemAssigned"
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  dynamic "monitor_metrics" {
    for_each = local.deploy_observability_tools ? [1] : []
    content {
    }
  }

  dynamic "oms_agent" {
    for_each = local.deploy_observability_tools ? [1] : []
    content {
      log_analytics_workspace_id      = azurerm_log_analytics_workspace.example[0].id
      msi_auth_for_monitoring_enabled = true
    }
  }

  lifecycle {
    ignore_changes = [
      monitor_metrics,
      azure_policy_enabled,
      microsoft_defender
    ]
  }

  web_app_routing {
    dns_zone_id = ""
  }
}
