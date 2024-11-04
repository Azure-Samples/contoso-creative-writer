## Azure Credentials:

# CREDENTIALS

++Username     = "@lab.CloudPortalCredential(User1).Username"
Password     = "@lab.CloudPortalCredential(User1).Password"
AzureEnvName = "AITOUR@lab.LabInstance.Id"
Subscription = "@lab.CloudSubscription.Id"++


**If you are viewing this from the Skillable lab page** the above are your unique azure credentials.

> **Note**: You will be asked to copy the above block in the lab later so keep this information readily available.

**If you are viewing this from Github:** The above are not your credentials. They are placeholders. Your actual credentials can be seen on the Skillable lab page.

***

### Welcome to this Microsoft workshop!

In this session, you will learn how to build the app, **Contoso Creative Writer**. This app will assist the marketing team at Contoso Outdoors in creating trendy, well-researched articles to promote the company’s products.

### Pre-Requisites

To participate in this workshop, you will need:

1. Your own laptop.
    * It need only be capable of running a browser and GitHub Codespaces, so almost any laptop will do.
    * A recent version of Edge, Chrome or Safari is recommended.
2. A GitHub Account.
    * If you don't have one, you can [signup for a free account](https://github.com/signup) now.
    * After this workshop is complete, you will have a fork of the "contoso-creative-writer" repository in your GitHub account, which includes all the materials you will need to reproduce this workshop at home.


### To begin this lab follow these steps:

1. Confirm that you can see your **Azure Credentials** at the top of the page. 
    * You will use these to login to Azure Developer CLI (AZD) and Azure CLI (AZ) later. 

2.  Click on this link [https://aka.ms/contoso-creative-writer-codespace](https://aka.ms/contoso-creative-writer-codespace). This will take you to a page where you can open a Codespace for Contoso Creative Writer. 
    * If you are not logged into Github already you will need to login using **your own** GitHub account credentials. 

3. Click the green **<> Create codespace** button at the bottom of the page.
    * This will open a pre-built Codespace on main. 

4. Once your Codespace is ready:
    * In the file explorer look for the **docs** folder and in it open the **workshop** folder. 
    * Open the **LAB-SETUP.ipynb** file. 
    * Follow the instructions to get going!

Have fun building!🎉
