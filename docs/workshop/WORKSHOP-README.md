# WRK551 Build a multi-tasking assistant with Azure OpenAI

## Welcome to workshop WRK551!

(**Note:** If you can see hashtags (like this ##) on this page right click on the WORKSHOP-README.md tab above and select `open preview`!)

Building Large Language Model (LLM) applications​ is hard! Companies want to build AI solutions but how can they do this in a reliable, reproducible and observable way?​

Challenges with AI:  ​
- Getting LLM app to work with various real world inputs ​
- Debugging (local and production)​ to understand failures
- Setting up and managing production infrastructure automation

This workshop will introduce new tooling that provides practical solutions to these problems. 

## Part 1: Setting Up

These are instructions for the insructor led AI Tour session, you should have the Skillable Lab Manual open in a different tab.

We'll begin by logging in to Azure Developer CLI (azd) and Azure CLI (az).

1. Open a terminal window.

2. Sign in to Azure Developer CLI. 
    - Use the `username` and `password` from the lab manual when prompted to sign in with an email and password.

    ```shell
    azd auth login
    ```

3.  Then sign in with Azure CLI. Again, use the `username` and `password` from the lab manual. 
    - Press enter to select the default subscription when prompted.
    
    ```shell
    az login --use-device-code
    ```

4.  Get the environment variables for your resource group by running the below command and **Replace `AzureEnvName`** with the value given for it in the lab manual.  
    - When prompted select `Y` to create the environment
    - Press enter to select the default subscription. 
    - Finally choose the location **Canada East**
    
    ```shell
    azd env refresh -e AzureEnvName
    ```

5. Save the environment variables to a .env file. 

    ```shell
    azd env get-values > .env
    ```

6. Set the correct roles by running the roles bash script. 
    ```shell
    bash infra/hooks/roles.sh
    ```

7. Run the postprovision script that will install the needed packages and deploy your app resources.
    - Make sure to **Replace `AzureEnvName`** with the value given for it in the lab manual. 
    - This might take a while but should not take more than 5mins.  

    ```shell
    azd hooks run postprovision -e AZDEnvName
    ```

You are now ready to start understanding and building Contoso Creative Writer! 
 
## Part 2: Understanding and Building Contoso Creative Writer

Once you've succesfully run the commands above, navigate to the file explorer on the left of the codepsace and open the [workshop.ipynb](workshop.ipynb) file to continue the workshop! 
