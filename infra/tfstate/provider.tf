terraform {
  required_version = ">= 1.1.7, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.80.0"
    }
    azurecaf = {
      source  = "aztfmod/azurecaf"
      version = "~>1.2.24"
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
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

data "azurerm_subscription" "current" {}

# Make client_id, tenant_id, subscription_id and object_id variables
data "azurerm_client_config" "current" {}
