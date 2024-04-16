resource "azurerm_role_assignment" "aks_role" {
  count                            = try(local.is_default_workspace ? 0 : 1, 0)
  principal_id                     = azurerm_kubernetes_cluster.aks[0].kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr[0].id
  skip_service_principal_aad_check = true
}
