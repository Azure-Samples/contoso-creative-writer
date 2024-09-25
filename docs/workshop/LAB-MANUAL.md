@lab.Title

## Azure Credentials:

**Username/email:** ++@lab.CloudPortalCredential(User1).Username++

**Password:** ++@lab.CloudPortalCredential(User1).Password++

**AzureEnvName:** ++AITOUR@lab.LabInstance.Id++

**Subscription:** ++@lab.CloudSubscription.Id++

(**If you are viewing this from Github:** Note the above are not your credentials. Your actual credentials can be seen on the Skillable lab page!)

***

### Welcome to the AI Tour and workshop WRK551!

In this session, you will learn how to build the app, **Contoso Creative Writer**. This app will assist the marketing team at Contoso Outdoors in creating trendy, well-researched articles to promote the company’s products.

### Pre-Requisites

To participate in this workshop, you will need:

1. Your own laptop.
    * It need only be capable of running a browser and GitHub Codespaces, so almost any laptop will do.
    * A recent version of Edge, Chrome or Safari is recommended.
2. A GitHub Account.
    * If you don't have one, you can [signup for a free account](https://github.com/signup) now.
    * After this workshop is complete, you will have a fork of the "contoso-creative-writer" repository in your GitHub account, which includes all the materials you will need to reproduce this workshop at home.
3. Familiarity with Visual Studio Code.
    * We will run all code in GitHub Codespaces, a virtualized Linux machine, instead of your local laptop. We won't be running anything on your laptop directly.
    * VS Code Online will be our development environment in GitHub Codespaces.
    * If you are familiar with running Codespaces within VS Code Desktop on your laptop, feel free to do so.
4. (preferred) Familiarity with the *bash* shell.
    * We'll be using *bash* to run commands in the VS Code terminal.

### To begin this lab follow these steps:

1. Confirm that you can see your **Azure Credentials** at the top of the page. You will use these to login to Azure Developer CLI and Azure CLI once Github Codespaces is set up. 

2. Open the Github Codespace by clicking this link: [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/contoso-creative-writer/).You may need to login using **your own** GitHub account credentials, if you are not logged in already. 


4. Navigate to [docs/workshop/WORKSHOP-README.md](WORKSHOP-README.md) and follow the instructions to get going!
    * When following the steps in Part 1 of the workshop Readme, use the [azure credentials](#azure-credentials) at the top of this manual to login and run the commands mentioned.

Have fun building!🎉