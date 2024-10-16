#!/usr/bin/env pwsh

# Set the script to exit on any error
$ErrorActionPreference = 'Stop'

Write-Output "Outputting environment variables to .env file..."
azd env get-values > .env

# Retrieve service names, resource group name, and other values from environment variables
$resourceGroupName = $env:AZURE_RESOURCE_GROUP
$searchService = $env:AZURE_SEARCH_NAME
$openAiService = $env:AZURE_OPENAI_NAME
$subscriptionId = $env:AZURE_SUBSCRIPTION_ID

# Ensure all required environment variables are set
if ([string]::IsNullOrEmpty($resourceGroupName) -or [string]::IsNullOrEmpty($searchService) -or [string]::IsNullOrEmpty($openAiService) -or [string]::IsNullOrEmpty($subscriptionId)) {
    Write-Host "One or more required environment variables are not set."
    Write-Host "Ensure that AZURE_RESOURCE_GROUP, AZURE_SEARCH_NAME, AZURE_OPENAI_NAME, AZURE_SUBSCRIPTION_ID are set."
    exit 1
}

# Set additional environment variables expected by app
# TODO: Standardize these and remove need for setting here
azd env set AZURE_OPENAI_API_VERSION 2023-03-15-preview
azd env set AZURE_OPENAI_CHAT_DEPLOYMENT gpt-35-turbo
azd env set AZURE_SEARCH_ENDPOINT $env:AZURE_SEARCH_ENDPOINT
azd env set REACT_APP_API_BASE_URL $env:WEB_SERVICE_ACA_URI

# Setup to run notebooks
# Retrieve the internalId of the Cognitive Services account
$INTERNAL_ID = az cognitiveservices account show `
    --name $env:AZURE_OPENAI_NAME `
    --resource-group $env:AZURE_RESOURCE_GROUP `
    --query "properties.internalId" -o tsv

# Construct the URL
$COGNITIVE_SERVICE_URL = "https://oai.azure.com/portal/$INTERNAL_ID?tenantid=$env:AZURE_TENANT_ID"

Write-Host "--- ✅ | 1. Post-provisioning - env configured ---"

# Setup to run notebooks
Write-Host 'Installing dependencies from "requirements.txt"'
python -m pip install -r src/api/requirements.txt > $null
python -m pip install ipython ipykernel > $null      # Install ipython and ipykernel
ipython kernel install --name=python3 --user > $null # Configure the IPython kernel
jupyter kernelspec list > $null                      # Verify kernelspec list isn't empty
Write-Host "--- ✅ | 2. Post-provisioning - ready to execute notebooks ---"

# Populate data
Write-Host "Populating data ...."
jupyter nbconvert --execute --to python --ExecutePreprocessor.timeout=-1 data/create-azure-search.ipynb > $null

Write-Host "--- ✅ | 3. Post-provisioning - populated data ---"