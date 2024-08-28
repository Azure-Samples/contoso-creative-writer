# WRK551 Build a multi-tasking assistant with Azure OpenAI

## Welcome to workshop WRK551!

Building Large Language Model (LLM) applications​ is hard! Companies want to build AI solutions but how can they do this in a reliable, reproducible and observable way?​

Challenges with AI:  ​
- Getting LLM app to work with various real world inputs ​
- Debugging (local and production)​ to understand failures
- Setting up and managing production infrastructure automation

This workshop will introduce new tooling that provides practical solutions to these problems. 

We will focus on 4 learning outcomes:

1. Understanding agents and prompt engineering with Prompty 
2. Utilizing Prompty tracing for debugging and observabilty
3. Building and running Contoso Creative 
4. Setting up automated evaluations with Github Actions 

## Part 1: Setting Up

If you are participating in the insructor led AI Tour session you should have already completed the instructions in the Skillable manual. Once these steps are completed you are ready to get started understaning and building Contoso Creative Writer!

We'll begin by logging in to Azure Developer CLI (azd) and Azure CLI (az) using the Azure `username` and `password` assigned to you on the Instructions page of Skillable. You'll need to be logged into both azd and az to access the Azure resources needed. 

1. Open a terminal window.
2. Sign in to Azure Developer CLI 

    ```shell
    azd auth login
    ```

3.  Then sign in with Azure CLI 
    
    ```shell
    az login --use-device-code
    ```
 
## Part 2: Understanding and Building Contoso Creative 
Once you've succesfully signed into both of these, click the file icon to the left and open the `workshop.ipynb` file. 
This is a jupyter notebook and we will be using it and the terminal to understand and go through the rest of this workshop. 

