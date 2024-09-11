# WRK551 Build a multi-tasking assistant with Azure OpenAI

## Welcome to workshop WRK551!

Building Large Language Model (LLM) applications​ is hard! Companies want to build AI solutions but how can they do this in a reliable, reproducible and observable way?​

Challenges with AI:  ​
- Getting LLM app to work with various real world inputs ​
- Debugging (local and production)​ to understand failures
- Setting up and managing production infrastructure automation

This workshop will introduce new tooling that provides practical solutions to these problems. 

## Part 1: Setting Up

If you are participating in the insructor led AI Tour session you should have already completed the instructions in the Skillable manual. Once these steps are completed you are ready to get started understaning and building Contoso Creative Writer!

We'll begin by logging in to Azure Developer CLI (azd) and Azure CLI (az) using the Azure `username` and `password` assigned to you on the Instructions page of Skillable. You'll need to be logged into both azd and az to access the Azure resources needed. 

1. Open a terminal window.
2. Sign in to Azure Developer CLI. Make sure to use the `username` and `password` from the lab manual when prompted. 

    ```shell
    azd auth login
    ```

3.  Then sign in with Azure CLI. Make sure to use the `username` and `password` from the lab manual when prompted. 
    
    ```shell
    az login --use-device-code
    ```

4.  Get the environment variables for your resource group. 
    - Make sure to **Replace `AzureEnvName`** with the resource group name in the lab manual.  
    - When prompted select Y to create the environment
    - Presee enter to select the default subscription. 
    - Finally choose the location **Canada East**
    
    ```shell
    azd env refresh -e AzureEnvName
    ```

5.  Run the post provision script. 
    - Make sure to **Replace `AzureEnvName`** with the resource group name in the lab manual.  

    ```shell
    azd hooks run postprovision -e AzureEnvName
    ```

6. Save the environment variables to a .env file. 

    ```shell
    azd env get-values > .env
    ```

7. Set the correct roles by running the roles bash script. 
    ```shell
    bash infra/hooks/roles.sh
    ```

8. Run the postprovision script that will install the needed packages and deploy your app resources.
    - Make sure to **Replace `AzureEnvName`** with the resource group name in the lab manual.  

    ```shell
    azd hooks run postprovision -e AZDEnvName
    ```

You now ready to start understanding and building Contoso Creative Writer! 
 
## Part 2: Understanding and Building Contoso Creative Writer
Once you've succesfully signed into both of these, click the file icon to the left and open the `workshop.ipynb` file. 
This is a jupyter notebook and we will be using it and the terminal to understand and go through the rest of this workshop. 

