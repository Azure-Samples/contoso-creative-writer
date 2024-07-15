
resource "azurerm_role_assignment" "aks_acr_role" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = azurerm_kubernetes_cluster.aks[0].kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr[0].id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "openai_backend" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = azurerm_user_assigned_identity.uai.principal_id
  role_definition_name             = "Cognitive Services OpenAI User"
  scope                            = azurerm_cognitive_account.cog.id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "openai_user" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = var.principal_id
  role_definition_name             = "Cognitive Services OpenAI User"
  scope                            = azurerm_cognitive_account.cog.id
}

resource "azurerm_role_assignment" "aisearchdata_backend" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = azurerm_user_assigned_identity.uai.principal_id
  role_definition_name             = "Search Index Data Contributor"
  scope                            = azurerm_search_service.search.id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "aisearchdata_user" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = var.principal_id
  role_definition_name             = "Search Index Data Contributor"
  scope                            = azurerm_search_service.search.id
}

resource "azurerm_role_assignment" "aisearchservice_backend" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = azurerm_user_assigned_identity.uai.principal_id
  role_definition_name             = "Search Service Contributor"
  scope                            = azurerm_search_service.search.id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "aisearchservice_user" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = var.principal_id
  role_definition_name             = "Search Service Contributor"
  scope                            = azurerm_search_service.search.id
}
