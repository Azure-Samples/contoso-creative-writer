set -e

# Output environment variables to .env file using azd env get-values
azd env get-values > .env

# Load variables from .env file
if [ -f .env ]; then
    source .env
else
    echo ".env file not found!"
    exit 1
fi

PRINCIPAL_ID=$(az ad signed-in-user show --query id -o tsv)

az role assignment create \
        --role "Storage Blob Data Contributor" \
        --assignee-object-id "${PRINCIPAL_ID}" \
        --scope /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${AZURE_OPENAI_RESOURCE_GROUP}" \
        --assignee-principal-type 'User'

az role assignment create \
    --role "Storage Blob Data Contributor" \
    --scope /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${AZURE_OPENAI_RESOURCE_GROUP}" \
    --assignee-principal-type 'User' \
    --assignee-object-id "${PRINCIPAL_ID}"