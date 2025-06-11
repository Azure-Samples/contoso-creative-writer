#!/bin/bash

set -e

# Output environment variables to .env file using azd env get-values
azd env get-values > .env

# Retrieve service names, resource group name, and other values from environment variables
resourceGroupName=$(azd env get-value AZURE_RESOURCE_GROUP)
searchService=$(azd env get-value AZURE_SEARCH_NAME)
openAiService=$(azd env get-value AZURE_OPENAI_NAME)
subscriptionId=$(azd env get-value AZURE_SUBSCRIPTION_ID)

# Ensure all required environment variables are set
if [ -z "$resourceGroupName" ] || [ -z "$searchService" ] || [ -z "$openAiService" ] || [ -z "$subscriptionId" ]; then
    echo "One or more required environment variables are not set."
    echo "Ensure that AZURE_RESOURCE_GROUP, AZURE_SEARCH_NAME, AZURE_OPENAI_NAME, AZURE_SUBSCRIPTION_ID are set."
    exit 1
fi

# Setup to run notebooks

echo "--- ✅ | 1. Post-provisioning - env configured ---"

# Setup to run notebooks
echo 'Installing dependencies from "requirements.txt"'
python3 -m pip install -r src/api/requirements.txt > /dev/null
python3 -m pip install ipython ipykernel > /dev/null      # Install ipython and ipykernel
ipython kernel install --name=python3 --user > /dev/null # Configure the IPython kernel
jupyter kernelspec list > /dev/null                      # Verify kernelspec list isn't empty
echo "--- ✅ | 2. Post-provisioning - ready execute notebooks ---"

echo "Populating data ...."
jupyter nbconvert --execute --to python --ExecutePreprocessor.timeout=-1 data/create-azure-search.ipynb > /dev/null

echo "--- ✅ | 3. Post-provisioning - populated data ---"
