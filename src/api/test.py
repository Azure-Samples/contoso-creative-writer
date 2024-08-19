import logging
import os

import azure.identity
import openai
from dotenv import load_dotenv

load_dotenv()
# Change to logging.DEBUG for more verbose logging from Azure and OpenAI SDKs
logging.basicConfig(level=logging.WARNING)


# if not os.getenv("AZURE_OPENAI_NAME") or not os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"):
#     logging.warning("AZURE_OPENAI_SERVICE and AZURE_OPENAI_GPT_DEPLOYMENT environment variables are empty. See README.")
#     exit(1)


credential = azure.identity.DefaultAzureCredential()
token_provider = azure.identity.get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

client = openai.AzureOpenAI(
    api_version="2023-07-01-preview",
    azure_endpoint="https://aoai-z4kxyuoouumm2.cognitiveservices.azure.com/",
    azure_ad_token_provider=token_provider,
)

response = client.chat.completions.create(
    # For Azure OpenAI, the model parameter must be set to the deployment name
    model=os.getenv("gpt-35-turbo"),
    temperature=0.7,
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that makes lots of cat references and uses emojis."},
        {"role": "user", "content": "Write a haiku about a hungry cat who wants tuna"},
    ],
)

print("Response: ")
print(response.choices[0].message.content)
