# Creative Writing Assistant: Working with Agents using Promptflow (Python Implementation) 

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/agent-openai-python-prompty) [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/azure-samples/agent-openai-python-prompty) 

This sample demonstrates how to create and work with AI agents driven by [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/). It includes a Flask app that takes a topic and instruction from a user then calls a research agent that uses the [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api) to research the topic, a product agent that uses [Azure AI Search](https://azure.microsoft.com/en-gb/products/ai-services/ai-search) to do a semantic similarity search for related products from a vectore store, a writer agent to combine the research and product information into a helpful article, and an editor agent to refine the article that's finally presented to the user.

## Table of Contents

- [Features](#features)
- [Azure account requirements](#azure-account-requirements)
- [Opening the project](#opening-the-project)
    - [GitHub Codespaces](#github-codespaces)
    - [VS Code Dev Containers](#vs-code-dev-containers)
    - [Local environment](#local-environment)
      - [Prerequisites](#prerequisites)
      - [Initializing the project](#initializing-the-project)
- [Deployment](#deployment)
- [Testing the sample](#testing-the-sample)
    - [Evaluating prompt flow results](#evaluating-prompt-flow-results)
- [Costs](#costs)
- [Security Guidelines](#security-guidelines)
- [Resources](#resources)
- [Code of Conduct](#code-of-conduct)

## Features

This project template provides the following features:

* [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/) to drive the various agents
* [Prompty and Prompt Flow](https://microsoft.github.io/promptflow/how-to-guides/develop-a-prompty/index.html) to create, manage and evaluate the prompt into our code.
* [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api) to research the topic provided
* [Azure AI Search](https://azure.microsoft.com/en-gb/products/ai-services/ai-search) for performing semantic similarity search
  
![Architecture Digram](images/Creative_writing.png)

## Azure account requirements

**IMPORTANT:** In order to deploy and run this example, you'll need:

* **Azure account**. If you're new to Azure, [get an Azure account for free](https://azure.microsoft.com/free/cognitive-search/) and you'll get some free Azure credits to get started. See [guide to deploying with the free trial](docs/deploy_lowcost.md).
* **Azure subscription with access enabled for the Azure OpenAI service**. You can request access with [this form](https://aka.ms/oaiapply). If your access request to Azure OpenAI service doesn't match the [acceptance criteria](https://learn.microsoft.com/legal/cognitive-services/openai/limited-access?context=%2Fazure%2Fcognitive-services%2Fopenai%2Fcontext%2Fcontext), you can use [OpenAI public API](https://platform.openai.com/docs/api-reference/introduction) instead.
    - Ability to deploy `gpt-35-turbo-0613` and `gpt-4-1106-Preview`.
    - We recommend using East US 2, as this region has access to all models and services required. 
* **Azure subscription with access enabled for [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)**
* **Azure subscription with access enabled for [Azure AI Search](https://azure.microsoft.com/en-gb/products/ai-services/ai-search)**

## Opening the project

You have a few options for setting up this project.
The easiest way to get started is GitHub Codespaces, since it will setup all the tools for you, but you can also [set it up locally](#local-environment).

### GitHub Codespaces

1. You can run this template virtually by using GitHub Codespaces. The button will open a web-based VS Code instance in your browser:
   
    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/agent-openai-python-prompty)

2. Open a terminal window.
3. Sign in to your Azure account:

    ```shell
    azd auth login
    ```

4. Provision the resources and deploy the code:

    ```shell
    azd up
    ```

    This project uses `gpt-35-turbo-0613` and `gpt-4-1106-Preview` which may not be available in all Azure regions. Check for [up-to-date region availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) and select a region during deployment accordingly. For this project we recommend East US 2.

5. Install the necessary Python packages:

    ```
    src/api
    pip install -r requirements.txt
    ```

Once the above steps are completed you can jump straight to [testing the sample](#testing-the-sample). 

### VS Code Dev Containers

A related option is VS Code Dev Containers, which will open the project in your local VS Code using the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

1. Start Docker Desktop (install it if not already installed)
2. Open the project:
   
    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/agent-openai-python-prompty.git)

3. In the VS Code window that opens, once the project files show up (this may take several minutes), open a terminal window.

4. Install required packages:

    ```shell
    cd src/api
    pip install -r requirements.txt
    ```
   Once you've completed these steps jump to [deployment](#deployment). 

### Local environment

#### Prerequisites

* [Azure Developer CLI (azd)](https://aka.ms/install-azd)
* [Python 3.10+](https://www.python.org/downloads/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git](https://git-scm.com/downloads)

**Note for Windows users:** If you are not using a container to run this sample, our hooks are currently all shell scripts. To provision this sample correctly while we work on updates we recommend using [git bash](https://gitforwindows.org/). 

#### Initializing the project

1. Create a new folder and switch to it in the terminal, then run this command to download the project code:

    ```shell
    azd init -t agent-openai-python-prompty
    ```
    Note that this command will initialize a git repository, so you do not need to clone this repository.

2. Install required packages:

    ```shell
    cd src/api
    pip install -r requirements.txt
    ```

## Deployment

Once you've opened the project in [Codespaces](#github-codespaces), [Dev Containers](#vs-code-dev-containers), or [locally](#local-environment), you can deploy it to Azure.

1. Sign in to your Azure account:

    ```shell
    azd auth login
    ```

    If you have any issues with that command, you may also want to try `azd auth login --use-device-code`.

    This will create a folder under `.azure/` in your project to store the configuration for this deployment. You may have multiple azd environments if desired.

2. Provision the resources and deploy the code:

    ```shell
    azd up
    ```

    This project uses `gpt-35-turbo-0613` and `gpt-4-1106-Preview` which may not be available in all Azure regions. Check for [up-to-date region availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) and select a region during deployment accordingly. We recommend using East US 2 for this project.

   After running azd up, you may be asked the following question during `Github Setup`:

   ```shell 
   Do you want to configure a GitHub action to automatically deploy this repo to Azure when you push code changes?
   (Y/n) Y
   ```

   You should respond with `N`, as this is not a necessary step, and take some time to setup. 


## Testing the sample

This sample repository contains an agents folder that includes subfolders for each agent. Each agent forlder contains a prompty file where the agents prompty is defined and a python file with the code used to run it. Exploring these files will help you understand what each agent is doing. The agents folder also contains an `orchestrator.py` file that can be used to run the entire flow and to create an article. When you ran `azd up` a catalogue of products was uploaded to the Azure AI Search vector store and index name `contoso-products` was created. 

To test the sample: 

1. Run the example web app locally using a Flask server. 

    First navigate to the src/api folder 
    ```
    cd ./src/api
    ```
    Run the Flask webserver
    ```
    flask --debug --app api.app:app run --port 8080
    ```

    If you open the server link in a browser, you will see a URL not found error, this is because we haven't created a home url route in flask. We have instead created a `/get_article` route which is used to pass context and instructions directly to the get_article.py file which runs the agent workflow.

   We have created a web interface which we will run next, but you can test the api is working as expected by running this in the browser:
    ```
    http://127.0.0.1:8080/get_article?context=Write an article about camping in alaska&instructions=find specifics about what type of gear they would need and explain in detail
    ```

2. Once the flask server is running you can now run the web app. To do this open a new terminal window and navigate to the web folder using this command:
    ```
    cd src/web
    ```
    First install node packages:
    ```
    npm install
    ```

    Then run the web app with a local dev web server:
    ```
    npm run dev
    ```

    This will launch the app, where you can use example context and instructions to get started. 
    On the 'Creative Team' page you can examine the output of each agent by clicking on it. The app should look like this:

   The getting started tab to send your instructions and context to the prompt:
   
    ![getting started](images/get_started_page.png)

    The creative team tab that let's you follow and understand the agents workflow:
   
    ![creative team](images/creative_team_agents.png)

    The document tab that displays the article that was created:
   
    ![generated article](images/winter_article.png)

    Change the instructions and context to create an article of your choice. 

3. For debugging purposes you may want to test in Python using the orchestrator Logic

    To run the sample using just the orchestrator logic use the following command:

    ```
    cd ./src/api
    python -m api.agents.orchestrator

    ```

## Evaluating prompt flow results

To understand how well our prompt flow performs using defined metrics like **groundedness**, **coherence** etc we can evaluate the results. To evaluate the prompt flow, we need to be able to compare it to what we see as "good results" in order to understand how well it aligns with our expectations. 

We may be able to evaluate the flow manually (e.g., using Azure AI Studio) but for now, we'll evaluate this by running the prompt flow using **gpt-4** and comparing our performance to the results obtained there. To do this, follow the instructions and steps in the notebook `evaluate-chat-prompt-flow.ipynb` under the `eval` folder.

You can also view the evaluation metrics by running the following command from the src/api folder. 

Run evaluation:
```
python -m api.evaluate.evaluate
```

## Setting up CI/CD with GitHub actions

This template is setup to run CI/CD when you push changes to your repo. When CI/CD is configured, evaluations will in GitHub actions and then automatically deploy your app on push to main.

To set up CI/CD with GitHub actions on your repository, run the following command:
```
azd pipeline config
```

**Workaround to enable CI/CD:** in the output, look for the "Creating service principal" line and **Copy** the name of the service principal (looks like az-dev-<letters and numbers>), an example is  shown below:
```
...
(✓) Done: Creating service principal az-dev-05-19-2024-02-02-02 (62c51d5e-17f7-4b06-bfab-fza2a4e1e6d8)
...
```

This will create a service principal in your Azure subscription that your GitHub actions to use when running azd and evaluations.

You will need to add a role assignment of this service principal on your tfstate storage account. Open the Azure portal, and take following steps:
  1. In the search box at the top of the screen, search for _ENVIRONMENT_NAME-tfstate_
  1. Select the resource group that appears
  1. Click to open the storage account in that resource group
  1. Select the **Access control (IAM)** on the left nav
  1. Then click **Add** > **Role Assignment**
  1. Search for the **Storage Blob Data Contributor** role, and select **Next**
  1. Click **+ Select Members**, and add the **az-dev-** role that you copied earlier
  1. Click **Review + Assign** twice

Currently, when your GitHub action runs, **it will remove your access** to call the OpenAI and AI Search resources from your development environment with your user identity. It essentially takes over this azd environment for CI/CD purposes, and if you want to continue working on this repo you should create a new development environment.

If you do want to re-enable access from your development environment, re-run the provision command:

```
azd provision
```

## Costs

Pricing may vary per region and usage. Exact costs cannot be estimated.
You may try the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) for the resources below:

* Azure Container Apps: Pay-as-you-go tier. Costs based on vCPU and memory used. [Pricing](https://azure.microsoft.com/pricing/details/container-apps/)
* Azure OpenAI: Standard tier, GPT and Ada models. Pricing per 1K tokens used, and at least 1K tokens are used per question. [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
* Azure Monitor: Pay-as-you-go tier. Costs based on data ingested. [Pricing](https://azure.microsoft.com/pricing/details/monitor/)

## Security Guidelines

This template use [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) built in to eliminate the need for developers to manage these credentials. Applications can use managed identities to obtain Microsoft Entra tokens without having to manage any credentials. We also use Key Vault, specifically for Bing Search, since Managed Identity is currently not implemented for it. Additionally, we have added a [GitHub Action tool](https://github.com/microsoft/security-devops-action) that scans the infrastructure-as-code files and generates a report containing any detected issues. To ensure best practices in your repo we recommend anyone creating solutions based on our templates ensure that the [Github secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) setting is enabled in your repos.

## Resources

* [Promptflow/Prompty Documentation](https://microsoft.github.io/promptflow/reference/python-library-reference/promptflow-core/promptflow.core.html?highlight=prompty#promptflow.core.Prompty)
* [Develop Python apps that use Azure AI services](https://learn.microsoft.com/azure/developer/python/azure-ai-for-python-developers)

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).

Resources:

- [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)
- [Microsoft Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
- Contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with questions or concerns


For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
