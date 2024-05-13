#!/bin/bash

# Convert WORKSPACE to lowercase and trim any whitespace
WORKSPACE=${WORKSPACE:-"azure"} # Set default value if not set
WORKSPACE=$(echo "${WORKSPACE}" | tr '[:upper:]' '[:lower:]' | xargs) # Convert to lowercase and trim whitespace

# Check if WORKSPACE is set to "azure"
if [ -z "$GITHUB_WORKSPACE" ] && [ "$WORKSPACE" = "azure" ]; then
    # Add a delay to ensure that the service is up and running
    echo "Waiting for the service to be available..."
    sleep 30
    
    # Check if AZD_PIPELINE_CONFIG_PROMPT is not set or is true
    if [ -z "${AZD_PIPELINE_CONFIG_PROMPT}" ] || [ "${AZD_PIPELINE_CONFIG_PROMPT}" = "true" ]; then
        
        echo "======================================================"
        echo "                     Github Action Setup                 "
        echo "======================================================"
        
        # Ask the user a question and get their response
        read -p "Do you want to configure a GitHub action to automatically deploy this repo to Azure when you push code changes? (Y/n) " response

        # Default response is "N"
        response=${response:-Y}

        # Check the response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo "Configuring GitHub Action..."
            azd auth login --scope https://graph.microsoft.com/.default
            azd pipeline config
            # Set AZD_GH_ACTION_PROMPT to false
            azd env set AZD_PIPELINE_CONFIG_PROMPT false
        fi
    fi

    echo "Retrieving the external IP address of the service"
    echo "======================================================"
    echo " Website IP Address                 "
    echo "======================================================"
    WEB_IP=$(kubectl get ingress ingress-web -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    echo "WEB IP: http://$WEB_IP"
fi