import os
import json
from typing import Dict
from openai import AzureOpenAI

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from api.agents.product.ai_search import retrieve_documentation
from openai import AzureOpenAI
from promptflow.tracing import trace

from dotenv import load_dotenv

load_dotenv()

@trace
def get_context(request, embedding):
    return retrieve_documentation(request=request, index_name="contoso-products", embedding=embedding)

def get_embedding(request: str):
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_ad_token_provider=token_provider
    )

    return client.embeddings.create(
            input=request,
            model="text-embedding-ada-002"
        ).data[0].embedding

def get_products(request: str) -> Dict[str, any]:
    embedding = get_embedding(request)
    products = get_context(request, embedding)
    return products

if __name__ == "__main__":
    context = "what kind of jackets do you have?"
    answer = get_products(context)
    print(json.dumps(answer, indent=2))
