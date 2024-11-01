targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name which is used to generate a short unique hash for each resource')
param environmentName string

@allowed([
  'canadaeast'
  'eastus'
  'eastus2'
  'northcentralus'
  'southcentralus'
  'swedencentral'
  'westus'
  'westus3'
])
@minLength(1)
@description('Primary location for all resources')
@metadata({
  azd: {
    type: 'location'
  }
})
param location string

param containerRegistryName string = ''
param aiHubName string = ''
@description('The Azure AI Studio project name. If ommited will be generated')
param aiProjectName string = ''
@description('The application insights resource name. If ommited will be generated')
param applicationInsightsName string = ''
@description('The Open AI resource name. If ommited will be generated')
param openAiName string = ''
@description('The Open AI connection name. If ommited will use a default value')
param openAiConnectionName string = ''
@description('The Open AI content safety connection name. If ommited will use a default value')
param openAiContentSafetyConnectionName string = ''
param keyVaultName string = ''
@description('The Azure Storage Account resource name. If ommited will be generated')
param storageAccountName string = ''

var abbrs = loadJsonContent('./abbreviations.json')
@description('The log analytics workspace name. If ommited will be generated')
param logAnalyticsWorkspaceName string = ''
param useApplicationInsights bool = true
param useContainerRegistry bool = true
param useSearch bool = true
var aiConfig = loadYamlContent('./ai.yaml')
@description('The name of the machine learning online endpoint. If ommited will be generated')
param endpointName string = ''
@description('The name of the azd service to use for the machine learning endpoint')
param endpointServiceName string = 'chat'
param resourceGroupName string = ''

@description('The Azure Search connection name. If ommited will use a default value')
param searchConnectionName string = ''

@description('The API version of the OpenAI resource')
param openAiApiVersion string = '2023-07-01-preview'

@description('The type of the OpenAI resource')
param openAiType string = 'azure'

@description('The name of the search service')
param searchServiceName string = ''

@description('The name of the bing search service')
param bingSearchName string = ''

@description('The name of the AI search index')
param aiSearchIndexName string = 'contoso-products'

@description('The name of the 35 turbo OpenAI deployment')
param openAi_35_turbo_DeploymentName string = 'gpt-35-turbo'


@description('The name of the 4 OpenAI deployment')
param openAi_4_DeploymentName string = 'gpt-4'


@description('The name of the 4 eval OpenAI deployment')
param openAi_4_eval_DeploymentName string = 'gpt-4-evals'

@description('The name of the OpenAI embedding deployment')
param openAiEmbeddingDeploymentName string = 'text-embedding-ada-002'

@description('Id of the user or app to assign application roles')
param principalId string = ''

@description('Whether the deployment is running on GitHub Actions')
param runningOnGh string = ''

@description('Whether the deployment is running on Azure DevOps Pipeline')
param runningOnAdo string = ''

var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

// USER ROLES
var principalType = empty(runningOnGh) && empty(runningOnAdo) ? 'User' : 'ServicePrincipal'
module managedIdentity 'core/security/managed-identity.bicep' = {
  name: 'managed-identity'
  scope: resourceGroup
  params: {
    name: 'id-${resourceToken}'
    location: location
    tags: tags
  }
}

module ai 'core/host/ai-environment.bicep' = {
  name: 'ai'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    hubName: !empty(aiHubName) ? aiHubName : 'ai-hub-${resourceToken}'
    projectName: !empty(aiProjectName) ? aiProjectName : 'ai-project-${resourceToken}'
    keyVaultName: !empty(keyVaultName) ? keyVaultName : '${abbrs.keyVaultVaults}${resourceToken}'
    storageAccountName: !empty(storageAccountName)
      ? storageAccountName
      : '${abbrs.storageStorageAccounts}${resourceToken}'
    openAiName: !empty(openAiName) ? openAiName : 'aoai-${resourceToken}'
    openAiConnectionName: !empty(openAiConnectionName) ? openAiConnectionName : 'aoai-connection'
    openAiContentSafetyConnectionName: !empty(openAiContentSafetyConnectionName) ? openAiContentSafetyConnectionName : 'aoai-content-safety-connection'
    openAiModelDeployments: array(contains(aiConfig, 'deployments') ? aiConfig.deployments : [])
    logAnalyticsName: !useApplicationInsights
      ? ''
      : !empty(logAnalyticsWorkspaceName)
          ? logAnalyticsWorkspaceName
          : '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: !useApplicationInsights
      ? ''
      : !empty(applicationInsightsName) ? applicationInsightsName : '${abbrs.insightsComponents}${resourceToken}'
    containerRegistryName: !useContainerRegistry
      ? ''
      : !empty(containerRegistryName) ? containerRegistryName : '${abbrs.containerRegistryRegistries}${resourceToken}'
    searchServiceName: !useSearch ? '' : !empty(searchServiceName) ? searchServiceName : '${abbrs.searchSearchServices}${resourceToken}'
    searchConnectionName: !useSearch ? '' : !empty(searchConnectionName) ? searchConnectionName : 'search-service-connection'
  }
}

module bing 'core/bing/bing-search.bicep' = {
  name: 'bing'
  scope: resourceGroup
  params: {
    name: 'agent-bing-search'
    location: 'global'
  }
}

// Container apps host (including container registry)
module containerApps 'core/host/container-apps.bicep' = {
  name: 'container-apps'
  scope: resourceGroup
  params: {
    name: 'app'
    location: location
    tags: tags
    containerAppsEnvironmentName: 'agent-ca-env'
    containerRegistryName: ai.outputs.containerRegistryName
    logAnalyticsWorkspaceName: ai.outputs.logAnalyticsWorkspaceName
  }
}

module apiContainerApp 'app/api.bicep' = {
  name: 'api'
  scope: resourceGroup
  params: {
    name: 'agent-api'
    location: location
    tags: tags
    identityName: managedIdentity.outputs.managedIdentityName
    identityId: managedIdentity.outputs.managedIdentityClientId
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    openAi_35_turbo_DeploymentName: !empty(openAi_35_turbo_DeploymentName) ? openAi_35_turbo_DeploymentName : 'gpt-35-turbo'
    openAi_4_DeploymentName: !empty(openAi_4_DeploymentName) ? openAi_4_DeploymentName : 'gpt-4'
    openAi_4_eval_DeploymentName: !empty(openAi_4_eval_DeploymentName) ? openAi_4_eval_DeploymentName : 'gpt-4-evals'
    openAiEmbeddingDeploymentName: openAiEmbeddingDeploymentName
    openAiEndpoint: ai.outputs.openAiEndpoint
    openAiName: ai.outputs.openAiName
    openAiType: openAiType
    openAiApiVersion: openAiApiVersion
    aiSearchEndpoint: ai.outputs.searchServiceEndpoint
    aiSearchIndexName: aiSearchIndexName
    appinsights_Connectionstring: ai.outputs.applicationInsightsConnectionString
    bingApiEndpoint: bing.outputs.endpoint
    bingApiKey: bing.outputs.bingApiKey
  }
}

module webContainerApp 'app/web.bicep' = {
  name: 'web'
  scope: resourceGroup
  params: {
    name: 'agent-web'
    location: location
    tags: tags
    identityName: managedIdentity.outputs.managedIdentityName
    identityId: managedIdentity.outputs.managedIdentityClientId
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    apiEndpoint: apiContainerApp.outputs.SERVICE_ACA_URI
  }
}

module aiSearchRole 'core/security/role.bicep' = {
  scope: resourceGroup
  name: 'ai-search-index-data-contributor'
  params: {
    principalId: managedIdentity.outputs.managedIdentityPrincipalId
    roleDefinitionId: '8ebe5a00-799e-43f5-93ac-243d3dce84a7' //Search Index Data Contributor
    principalType: 'ServicePrincipal'
  }
}


module appinsightsAccountRole 'core/security/role.bicep' = {
  scope: resourceGroup
  name: 'appinsights-account-role'
  params: {
    principalId: managedIdentity.outputs.managedIdentityPrincipalId
    roleDefinitionId: '3913510d-42f4-4e42-8a64-420c390055eb' // Monitoring Metrics Publisher
    principalType: 'ServicePrincipal'
  }
}

module userAiSearchRole 'core/security/role.bicep' = if (!empty(principalId)) {
  scope: resourceGroup
  name: 'user-ai-search-index-data-contributor'
  params: {
    principalId: principalId
    roleDefinitionId: '8ebe5a00-799e-43f5-93ac-243d3dce84a7' //Search Index Data Contributor
    principalType: principalType
  }
}

module searchRoleUser 'core/security/role.bicep' = {
  scope: resourceGroup
  name: 'search-role-user'
  params: {
    principalId: principalId
    roleDefinitionId: '1407120a-92aa-4202-b7e9-c0e197c71c8f'
    principalType: principalType
  }
}

module searchContribRoleUser 'core/security/role.bicep' = {
  scope: resourceGroup
  name: 'search-contrib-role-user'
  params: {
    principalId: principalId
    roleDefinitionId: '8ebe5a00-799e-43f5-93ac-243d3dce84a7'
    principalType: principalType
  }
}

module searchSvcContribRoleUser 'core/security/role.bicep' = {
  scope: resourceGroup
  name: 'search-svccontrib-role-user'
  params: {
    principalId: principalId
    roleDefinitionId: '7ca78c08-252a-4471-8644-bb5ff32d4ba0'
    principalType: principalType
  }
}

module openaiRoleUser 'core/security/role.bicep' = if (!empty(principalId)) {
  scope: resourceGroup
  name: 'user-openai-user'
  params: {
    principalId: principalId
    roleDefinitionId: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd' //Cognitive Services OpenAI User
    principalType: principalType
  }
}

output AZURE_LOCATION string = location
output AZURE_RESOURCE_GROUP string = resourceGroup.name

output AZURE_OPENAI_35_TURBO_DEPLOYMENT_NAME string = openAi_35_turbo_DeploymentName
output AZURE_OPENAI_DEPLOYMENT_NAME string = openAi_4_DeploymentName
output AZURE_OPENAI_4_EVAL_DEPLOYMENT_NAME string = openAi_4_eval_DeploymentName
output AZURE_OPENAI_API_VERSION string = openAiApiVersion
output AZURE_OPENAI_ENDPOINT string = ai.outputs.openAiEndpoint
output AZURE_OPENAI_NAME string = ai.outputs.openAiName
output AZURE_OPENAI_RESOURCE_GROUP string = resourceGroup.name
output AZURE_AI_PROJECT_NAME string = ai.outputs.projectName
output AZURE_OPENAI_RESOURCE_GROUP_LOCATION string = resourceGroup.location

output API_SERVICE_ACA_NAME string = apiContainerApp.outputs.SERVICE_ACA_NAME
output API_SERVICE_ACA_URI string = apiContainerApp.outputs.SERVICE_ACA_URI
output API_SERVICE_ACA_IMAGE_NAME string = apiContainerApp.outputs.SERVICE_ACA_IMAGE_NAME

output WEB_SERVICE_ACA_NAME string = webContainerApp.outputs.SERVICE_ACA_NAME
output WEB_SERVICE_ACA_URI string = webContainerApp.outputs.SERVICE_ACA_URI
output WEB_SERVICE_ACA_IMAGE_NAME string = webContainerApp.outputs.SERVICE_ACA_IMAGE_NAME

output AZURE_CONTAINER_ENVIRONMENT_NAME string = containerApps.outputs.environmentName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName

output APPINSIGHTS_CONNECTIONSTRING string = ai.outputs.applicationInsightsConnectionString

output OPENAI_TYPE string = 'azure'
output AZURE_EMBEDDING_NAME string = openAiEmbeddingDeploymentName

output AZURE_SEARCH_ENDPOINT string = ai.outputs.searchServiceEndpoint
output AZURE_SEARCH_NAME string = ai.outputs.searchServiceName

output BING_SEARCH_ENDPOINT string = bing.outputs.endpoint
output BING_SEARCH_KEY string = bing.outputs.bingApiKey


