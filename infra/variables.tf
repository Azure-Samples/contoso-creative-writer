variable "location" {
  type = string
}

variable "environment_name" {
  description = "The name of the azd environment to be deployed"
  type        = string
}

variable "principal_id" {
  description = "The Id of the azd service principal to add to deployed keyvault access policies"
  type        = string
  default     = ""
}

variable "workspace" {
  description = "value of workspace"
  type        = string
  default     = "dev"
}

variable "openai_model_name" {
  description = "value of azure openai model name"
  type        = string
  default     = "gpt-4"
}

variable "openai_model_version" {
  description = "value of azure openai model version"
  type        = string
  default     = "1106-Preview"
}

variable "openai_model_capacity" {
  description = "value of azure openai model capacity"
  type        = number
  default     = 30
}

variable "openai_35_turbo_model_name" {
  description = "value of azure openai model name"
  type        = string
  default     = "gpt-35-turbo"
}

variable "openai_4_eval_deployment_name" {
  description = "value of azure openai model name"
  type        = string
  default     = "gpt-4-eval"
}

variable "openai_4_eval_model_name" {
  description = "value of azure openai model name"
  type        = string
  default     = "gpt-4"
}


variable "openai_4_eval_model_version" {
  description = "value of azure openai model name"
  type        = string
  default     = "0613"
}

variable "openai_4_eval_model_capacity" {
  description = "value of azure openai model capacity"
  type        = number
  default     = 20
}


variable "openai_35_turbo_model_version" {
  description = "value of azure openai model version"
  type        = string
  default     = "0613"
}

variable "openai_35_turbo_model_capacity" {
  description = "value of azure openai model capacity"
  type        = number
  default     = 30
}

variable "openai_embedding_model_name" {
  description = "value of azure openai model name"
  type        = string
  default     = "text-embedding-ada-002"
}

variable "openai_embedding_model_version" {
  description = "value of azure openai model version"
  type        = string
  default     = "2"
}

variable "openai_embedding_model_capacity" {
  description = "value of azure openai model capacity"
  type        = number
  default     = 30
}


variable "openai_api_version" {
  description = "value of azure openai api version"
  type        = string
  default     = "2023-12-01-preview"
}
variable "search_index_name" {
  description = "value of search index name"
  type        = string
  default     = "docs"
}

variable "vectordb_type" {
  description = "value of vectordb type"
  type        = string
  default     = "azure_search"
}
variable "k8s_namespace" {
  description = "value of kubernetes namespace"
  type        = string
  default     = "default"
}

variable "log_analytics_workspace_sku" {
  description = "log analytics sku"
  type        = string
  default     = "PerGB2018"
}

variable "deploy_observability_tools" {
  description = "value of setting to deploy observability stack which includes prometheus, grafana, and container insights. this string value will be used to set the local boolean variable"
  type        = string
  default     = "true"
}
