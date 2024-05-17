import os
import json
from typing import Dict, List
from openai import AzureOpenAI

from api.agents.product.ai_search import retrieve_documentation
from openai import AzureOpenAI
from promptflow.tracing import trace

from dotenv import load_dotenv

load_dotenv()

@trace
def get_context(question, embedding):
    return retrieve_documentation(question=question, index_name="contoso-products", embedding=embedding)

def get_embedding(question: str):
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version=os.environ["AZURE_OPENAI_API_VERSION"]
    )

    return client.embeddings.create(
            input=question,
            model="text-embedding-ada-002"
        ).data[0].embedding


def get_products(context: str) -> Dict[str, any]:
    embedding = get_embedding(context)
    products = get_context(context, embedding)
    print(products)
    return products


if __name__ == "__main__":
    context = "what kind of jackets do you have?"
    answer = get_products(context)
    print(json.dumps(answer, indent=2))
