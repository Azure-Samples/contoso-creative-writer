param name string
param location string = resourceGroup().location
param tags object = {}

param identityName string
param identityId string
param containerAppsEnvironmentName string
param containerRegistryName string
param serviceName string = 'api'
param openAi_35_turbo_DeploymentName string
param openAi_4_DeploymentName string
param openAi_4_eval_DeploymentName string
param openAiEndpoint string
param openAiName string
param openAiApiVersion string
param openAiEmbeddingDeploymentName string
param openAiType string
param aiSearchEndpoint string
param aiSearchIndexName string
param appinsights_Connectionstring string

@secure()
param bingApiKey string
param bingApiEndpoint string


module app '../core/host/container-app-upsert.bicep' = {
  name: '${serviceName}-container-app-module'
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    identityName: identityName
    identityType: 'UserAssigned'
    containerAppsEnvironmentName: containerAppsEnvironmentName
    containerRegistryName: containerRegistryName
    secrets: {
      'bing-search-key': bingApiKey
    }
    env: [
      {
        name: 'AZURE_CLIENT_ID'
        value: identityId
      }
      {
        name: 'AZURE_SEARCH_ENDPOINT'
        value: aiSearchEndpoint
      }
      {
        name: 'AZUREAISEARCH__INDEX_NAME'
        value: aiSearchIndexName
      }
      {
        name: 'OPENAI_TYPE'
        value: openAiType
      }
      {
        name: 'AZURE_OPENAI_API_VERSION'
        value: openAiApiVersion
      }
      {
        name: 'AZURE_OPENAI_ENDPOINT'
        value: openAiEndpoint
      }
      {
        name: 'AZURE_OPENAI_NAME'
        value: openAiName
      }
      {
        name: 'AZURE_OPENAI_35_TURBO_DEPLOYMENT_NAME'
        value: openAi_35_turbo_DeploymentName
      }
      {
        name: 'AZURE_OPENAI_DEPLOYMENT_NAME'
        value: openAi_4_DeploymentName
      }
      {
        name: 'AZURE_OPENAI_4_EVAL_DEPLOYMENT_NAME'
        value: openAi_4_eval_DeploymentName
      }
      {
        name: 'AZURE_EMBEDDING_NAME'
        value: openAiEmbeddingDeploymentName
      }
      {
        name: 'APPINSIGHTS_CONNECTIONSTRING'
        value: appinsights_Connectionstring
      }
      {
        name: 'BING_SEARCH_ENDPOINT'
        value: bingApiEndpoint
      }
      {
        name: 'BING_SEARCH_KEY'
        secretRef: 'bing-search-key'
      }

    ]
    targetPort: 80
  }
}

output SERVICE_ACA_NAME string = app.outputs.name
output SERVICE_ACA_URI string = app.outputs.uri
output SERVICE_ACA_IMAGE_NAME string = app.outputs.imageName
