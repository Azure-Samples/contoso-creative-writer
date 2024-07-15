terraform {
  backend "azurerm" {}
  required_version = ">= 1.1.7, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.80.0"
    }

    azapi = {
      source  = "Azure/azapi"
      version = ">= 1.12.1"
    }

    azurecaf = {
      source  = "aztfmod/azurecaf"
      version = "~>1.2.24"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.3"
    }

    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.1.0"
    }

    local = {
      source  = "hashicorp/local"
      version = "=2.4.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "=3.5.1"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    cognitive_account {
      purge_soft_delete_on_destroy = true
    }
  }
}

provider "kubernetes" {
  host                   = local.is_default_workspace ? "" : azurerm_kubernetes_cluster.aks[0].kube_config.0.host
  client_certificate     = local.is_default_workspace ? "" : base64decode(azurerm_kubernetes_cluster.aks[0].kube_config.0.client_certificate)
  client_key             = local.is_default_workspace ? "" : base64decode(azurerm_kubernetes_cluster.aks[0].kube_config.0.client_key)
  cluster_ca_certificate = local.is_default_workspace ? "" : base64decode(azurerm_kubernetes_cluster.aks[0].kube_config.0.cluster_ca_certificate)
}

provider "helm" {
  debug = true
  kubernetes {
    host                   = local.is_default_workspace ? "" : azurerm_kubernetes_cluster.aks[0].kube_config.0.host
    client_certificate     = local.is_default_workspace ? "" : base64decode(azurerm_kubernetes_cluster.aks[0].kube_config.0.client_certificate)
    client_key             = local.is_default_workspace ? "" : base64decode(azurerm_kubernetes_cluster.aks[0].kube_config.0.client_key)
    cluster_ca_certificate = local.is_default_workspace ? "" : base64decode(azurerm_kubernetes_cluster.aks[0].kube_config.0.cluster_ca_certificate)
  }
}

data "azurerm_subscription" "current" {}

# Make client_id, tenant_id, subscription_id and object_id variables
data "azurerm_client_config" "current" {}
