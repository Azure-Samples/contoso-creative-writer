#!/bin/bash

azd env get-values > .env

# Retrieve the internalId of the Cognitive Services account
INTERNAL_ID=$(az cognitiveservices account show \
    --name ${AZURE_OPENAI_NAME} \
    -g ${AZURE_RESOURCE_GROUP} \
--query "properties.internalId" -o tsv)

# Construct the URL
COGNITIVE_SERVICE_URL="https://oai.azure.com/portal/${INTERNAL_ID}?tenantid=${AZURE_TENANT_ID}"

# Display OpenAI Endpoint and other details
echo "======================================================"
echo " AI Configuration                 "
echo "======================================================"
echo "    OpenAI Endpoint: ${AZURE_OPENAI_ENDPOINT}                    "
echo "    SKU Name: S0                             "
echo "    AI Model Name: ${AZURE_OPENAI_MODEL_NAME}                    "
echo "    Model Version: vision-preview                    "
echo "    Model Capacity: 120                "
echo "    Azure Portal Link:                                 "
echo "    https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${AZURE_RESOURCE_GROUP}/providers/Microsoft.CognitiveServices/accounts/${AZURE_OPENAI_NAME}/overview"
echo "    Azure OpenAI Studio: ${COGNITIVE_SERVICE_URL}    "
echo ""



echo "--- ✅ | 1. Post-provisioning - env configured ---"

# Setup to run notebooks
echo 'Installing dependencies from "./src/api/requirements.txt"'
python -m pip install -r requirements.txt > /dev/null
python -m pip install ipython ipykernel > /dev/null      # Install ipython and ipykernel
ipython kernel install --name=python3 --user > /dev/null # Configure the IPython kernel
jupyter kernelspec list > /dev/null                      # Verify kernelspec list isn't empty
echo "--- ✅ | 2. Post-provisioning - ready execute notebooks ---"

echo "Populating data ...."
jupyter nbconvert --execute --to python --ExecutePreprocessor.timeout=-1 data/create-azure-search.ipynb > /dev/null

echo "--- ✅ | 3. Post-provisioning - populated data ---"