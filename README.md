---
name: Creative Writing Assistant
description: Working with Agents using Promptflow (Python Implementation) 
languages:
- python
- typescript
- bicep
- azdeveloper
products:
- azure-openai
- bing-search
- azure-ai-search
- azure
page_type: sample
urlFragment: agent-openai-python-prompty
---

# Creative Writing Assistant: Working with Agents using Promptflow (Python Implementation) 

### Samples in JavaScript, Python, and Java. Learn more at [https://aka.ms/azai](https://aka.ms/azai).
---

## Table of Contents

- [Features](#features)
- [Azure account requirements](#azure-account-requirements)
- [Azure Deployment](#azure-deployment)
  - [Cost estimation](#cost-estimation)
  - [Project setup](#project-setup)
    - [GitHub Codespaces](#option-1-github-codespaces)
    - [VS Code Dev Containers](#option-2-vs-code-dev-containers)
    - [Local environment](#option-3-local-environment)
- [Deploying](#deploying)
- [Using the app](#using-the-app)
- [Evaluating prompt flow results](#evaluating-prompt-flow-results)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)


[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/Azure-Samples/agent-openai-python-prompty)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/agent-openai-python-prompty) 

This sample demonstrates how to create and work with AI agents. The app takes a topic and instruction input and then calls a research agent, writer agent, and editor agent. 

We will be using the creative writting assistant to find the latest camping trends and activities in winter. The `research agent` will recieve some context we provide and an instruction to find information on what we are looking for. It will use this information to create queries, which it will pass to the [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api) to search the web for relevant information to return. The `product agent` will also recieve the context we provided and will use [Azure AI Search](https://azure.microsoft.com/en-gb/products/ai-services/ai-search) to search through camping product information in a vector store and return the products that are semantically similar to the context. 

The research and products returned will be sent to the `writing agent`, along with the context and instructions we provided. The writer then uses all of this information to create an article. This article is passed to an `editor agent` that analyzes the article, provides feedback for writer and decides whether to accept or reject the article. If the article is rejected the feedback is sent to the researcher and writer agents and a new article is created that incoperates the feedback. In this sample the editor can only reject the article twice. The edited article is then returned to the user. 

This sample uses the **[Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)** to access the LLM that will drive the agents. It also leverages **[Prompty and Prompt Flow](https://microsoft.github.io/promptflow/how-to-guides/develop-a-prompty/index.html)** to create, manage and evaluate the prompts into the code. Prompty is a 'markdown-like' file with a `.prompty` extension for developing prompt templates. 

## Features

This project template provides the following features:

* An `Agents` folder with all the agents mentioned in the project description. Each agent subfolder is made up of a `.prompty` and `.py` file. 
* An `orchestrator.py` file where the agent workflow is defined. 
* `requirements.txt` file with all the python packages needed to run this example.
* An `app.py` file that enables you to run this application as a Flask app. 
* A `.env.sample` file to let you know which provisioned resources you will need to run this app. 
  

![Architecture Digram]()

## Azure account requirements

**IMPORTANT:** In order to deploy and run this example, you'll need:

* **Azure account**. If you're new to Azure, [get an Azure account for free](https://azure.microsoft.com/free/cognitive-search/) and you'll get some free Azure credits to get started. See [guide to deploying with the free trial](docs/deploy_lowcost.md).
* **Azure subscription with access enabled for the Azure OpenAI service**. You can request access with [this form](https://aka.ms/oaiapply). If your access request to Azure OpenAI service doesn't match the [acceptance criteria](https://learn.microsoft.com/legal/cognitive-services/openai/limited-access?context=%2Fazure%2Fcognitive-services%2Fopenai%2Fcontext%2Fcontext), you can use [OpenAI public API](https://platform.openai.com/docs/api-reference/introduction) instead.
    - Ability to deploy `gpt-35-turbo-0613` and `gpt-4-1106-Preview`.
    - We recommend using East US 2, as this region has access to all models and services required. 
* **Azure subscription with access enabled for [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)**
* * **Azure subscription with access enabled for [Azure AI Search](https://azure.microsoft.com/en-gb/products/ai-services/ai-search)**
* **Azure account permissions**:
  * Your Azure account must have `Microsoft.Authorization/roleAssignments/write` permissions, such as [Role Based Access Control Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#role-based-access-control-administrator-preview), [User Access Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#user-access-administrator), or [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#owner). If you don't have subscription-level permissions, you must be granted [RBAC](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#role-based-access-control-administrator-preview) for an existing resource group and [deploy to that existing group](docs/deploy_existing.md#resource-group).
  * Your Azure account also needs `Microsoft.Resources/deployments/write` permissions on the subscription level.

## Azure deployment

### Cost estimation

Pricing varies per region and usage, so it isn't possible to predict exact costs for your usage.
However, you can try the [Azure pricing calculator](https://azure.com/e/d18187516e9e421e925b3b311eec8aae) for the resources mentioned above.

### Project setup

You have a few options for setting up this project.
The easiest way to get started is GitHub Codespaces, since it will setup all the tools for you, but you can also set it up locally if desired.
Here are the three options in increasing order of complexity and effort on your part. 

Pick one!

 1. [GitHub Codespaces](#option-1-github-codespaces) (recommended)
 2. [VS Code Dev Containers](#option-2-vs-code-dev-containers) 
 3. [Local environment](#option-3-local-environment) 

#### Option 1: GitHub Codespaces

  **This is the recommended option!**
  You can run this repo virtually by using GitHub Codespaces, which will open a web-based VS Code in your browser. To run code spaces:
 - Fork the repo into your personal profile.
 - In your fork, click the green Code button on the repository
 - Select the `Codespaces` tab and click `Create codespace...`

 You can also click this button:
[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/Azure-Samples/agent-openai-python-prompty)

Once the codespace opens (this may take several minutes), open a terminal window.
Once you've launched Codespaces you can now [deploy this app](#deploying).

#### Option 2: VS Code Dev Containers

A related option is VS Code Dev Containers, which will open the project in your local VS Code using the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

1. Start Docker Desktop (install it if not already installed)
2. Open the project:
    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/agent-openai-python-prompty.git)
3. In the VS Code window that opens, once the project files show up (this may take several minutes), open a terminal window.

Once you've launched your docker container environment you can now [deploy this app](#deploying).

#### Option 3: Local environment

1. Install the required tools:

    * [Azure Developer CLI](https://aka.ms/azure-dev/install)
    * [Python 3.9, 3.10, or 3.11](https://www.python.org/downloads/)
      * **Important**: Python and the pip package manager must be in the path in Windows for the setup scripts to work.
      * **Important**: Ensure you can run `python --version` from console. On Ubuntu, you might need to run `sudo apt install python-is-python3` to link `python` to `python3`.
    * [Node.js 14+](https://nodejs.org/en/download/)
    * [Git](https://git-scm.com/downloads)
    * [Powershell 7+ (pwsh)](https://github.com/powershell/powershell) - For Windows users only.
      * **Important**: Ensure you can run `pwsh.exe` from a PowerShell terminal. If this fails, you likely need to upgrade PowerShell.

2. Create a new folder and switch to it in the terminal.
3. Run this command to download the project code:

    ```shell
    azd init -t agent-openai-python-prompty
    ```

    Note that this command will initialize a git repository, so you do not need to clone this repository.

### Deploying

Follow these steps to provision Azure resources and deploy the application code:

1. Login to your Azure account:

    ```shell
    azd auth login
    ```

2. Create a new azd environment:

    ```shell
    azd env new
    ```

    Enter a name that will be used for the resource group.
    This will create a new folder in the `.azure` folder, and set it as the active environment for any     calls to `azd` going forward.

3. Run:
   
   ```shell
    azd up
    ```
   This will provision Azure resources and deploy this sample to those resources.
   You will be prompted to select two locations, one for the majority of resources and one for the OpenAI resource, which is currently a short list. That location list is based on the [OpenAI model availability table](https://learn.microsoft.com/azure/cognitive-services/openai/concepts/models#model-summary-table-and-region-availability) and may become outdated as availability changes. For this sample we recommend using US East 2.


## Using the app

Change to api/agents folder:
```
cd src/api
```

To run just the orchestrator logic:
```
python -m api.agents.orchestrator
```

To run the flask webserver:
```
flask --debug --app api.app:app run --port 5000
```
```
http://127.0.0.1:5000/get_article?context=Write an article about camping in alaska&instruction=find specifics about what type of gear they would need and explain in detail
```

In a new terminal
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

Then run evaluation
```
cd evaluate
python evaluate.py
```
## Evaluating prompt flow results

Now, we need to understand how well our prompt flow performs using defined metrics like **groundedness**, **coherence** etc. To evaluate the prompt flow, we need to be able to compare it to what we see as "good results" in order to understand how well it aligns with our expectations. 

We may be able to evaluate the flow manually (e.g., using Azure AI Studio) but for now, we'll evaluate this by running the prompt flow using **gpt-4** and comparing our performance to the results obtained there. To do this, follow the instructions and steps in the notebook `evaluate-chat-prompt-flow.ipynb` under the `eval` folder.


## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).

Resources:

- [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)
- [Microsoft Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
- Contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with questions or concerns


For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
