#!/usr/bin/env pwsh

# Set the script to exit on any error
$ErrorActionPreference = 'Stop'

Write-Output "Outputting environment variables to .env file..."
azd env get-values > .env

# Retrieve service names, resource group name, and other values from environment variables
$resourceGroupName = (azd env get-value AZURE_RESOURCE_GROUP)
$searchService = (azd env get-value AZURE_SEARCH_NAME)
$openAiService = (azd env get-value AZURE_OPENAI_NAME)
$subscriptionId = (azd env get-value AZURE_SUBSCRIPTION_ID)

# Ensure all required environment variables are set
if ([string]::IsNullOrEmpty($resourceGroupName) -or [string]::IsNullOrEmpty($searchService) -or [string]::IsNullOrEmpty($openAiService) -or [string]::IsNullOrEmpty($subscriptionId)) {
    Write-Host "One or more required environment variables are not set."
    Write-Host "Ensure that AZURE_RESOURCE_GROUP, AZURE_SEARCH_NAME, AZURE_OPENAI_NAME, AZURE_SUBSCRIPTION_ID are set."
    exit 1
}

# Setup to run notebooks

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