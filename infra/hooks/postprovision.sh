#!/bin/bash

# Output environment variables to .env file using azd env get-values
azd env get-values > .env

acr_build () {
    image_name=$1
    aca_name=$2
    src_dir=$3
    target_port=$4
    image_fqn="${AZURE_CONTAINER_REGISTRY_NAME}.azurecr.io/${image_name}"
    echo  "Building ${image_name} using ${src_dir} ..."
    az acr build --subscription ${AZURE_SUBSCRIPTION_ID} --registry ${AZURE_CONTAINER_REGISTRY_NAME} --image ${image_name} ${src_dir}
    az containerapp update --subscription ${AZURE_SUBSCRIPTION_ID} --name ${aca_name} --resource-group ${AZURE_RESOURCE_GROUP} --image ${image_fqn}
    az containerapp ingress update --subscription ${AZURE_SUBSCRIPTION_ID} --name ${aca_name} --resource-group ${AZURE_RESOURCE_GROUP} --target-port ${target_port}
}

acr_build creativeagentapi:latest ${API_SERVICE_ACA_NAME} ./src/api/ 5000
acr_build creativeagentweb:latest ${WEB_SERVICE_ACA_NAME} ./src/web/ 80

# Retrieve service names, resource group name, and other values from environment variables
resourceGroupName=$AZURE_RESOURCE_GROUP
searchService=$AZURE_SEARCH_NAME
openAiService=$AZURE_OPENAI_NAME
subscriptionId=$AZURE_SUBSCRIPTION_ID

# Ensure all required environment variables are set
if [ -z "$resourceGroupName" ] || [ -z "$searchService" ] || [ -z "$openAiService" ] || [ -z "$subscriptionId" ]; then
    echo "One or more required environment variables are not set."
    echo "Ensure that AZURE_RESOURCE_GROUP, AZURE_SEARCH_NAME, AZURE_OPENAI_NAME, AZURE_SUBSCRIPTION_ID are set."
    exit 1
fi

# Set additional environment variables expected by app
# TODO: Standardize these and remove need for setting here
azd env set AZURE_OPENAI_API_VERSION 2023-03-15-preview
azd env set AZURE_OPENAI_CHAT_DEPLOYMENT gpt-35-turbo
azd env set AZURE_SEARCH_ENDPOINT $AZURE_SEARCH_ENDPOINT
azd env set REACT_APP_API_BASE_URL $WEB_SERVICE_ACA_URI

# Setup to run notebooks
# Retrieve the internalId of the Cognitive Services account
INTERNAL_ID=$(az cognitiveservices account show \
    --name ${AZURE_OPENAI_NAME} \
    -g ${AZURE_RESOURCE_GROUP} \
--query "properties.internalId" -o tsv)

# Construct the URL
COGNITIVE_SERVICE_URL="https://oai.azure.com/portal/${INTERNAL_ID}?tenantid=${AZURE_TENANT_ID}"

echo "--- ✅ | 1. Post-provisioning - env configured ---"

# Setup to run notebooks
echo 'Installing dependencies from "src/api/requirements.txt"'
python -m pip install -r src/api/requirements.txt > /dev/null
python -m pip install ipython ipykernel > /dev/null      # Install ipython and ipykernel
ipython kernel install --name=python3 --user > /dev/null # Configure the IPython kernel
jupyter kernelspec list > /dev/null                      # Verify kernelspec list isn't empty
echo "--- ✅ | 2. Post-provisioning - ready execute notebooks ---"

echo "Populating data ...."
jupyter nbconvert --execute --to python --ExecutePreprocessor.timeout=-1 data/create-azure-search.ipynb > /dev/null

echo "--- ✅ | 3. Post-provisioning - populated data ---"