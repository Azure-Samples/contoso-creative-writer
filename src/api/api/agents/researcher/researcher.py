import json
import os
import requests
import sys
import urllib.parse

from promptflow.tracing import trace
from promptflow.core import Prompty, AzureOpenAIModelConfiguration

from api.logging import log_output

from dotenv import load_dotenv
from pathlib import Path

folder = Path(__file__).parent.absolute().as_posix()
load_dotenv()

#bing does not currently support managed identity
BING_SEARCH_ENDPOINT = os.getenv("BING_SEARCH_ENDPOINT")
BING_SEARCH_KEY = os.getenv("BING_SEARCH_KEY")
BING_HEADERS = {"Ocp-Apim-Subscription-Key": BING_SEARCH_KEY}


def _make_endpoint(endpoint, path):
    """Make an endpoint URL"""
    return f"{endpoint}{'' if endpoint.endswith('/') else '/'}{path}"


def _make_request(path, params=None):
    """Make a request to the API"""
    endpoint = _make_endpoint(BING_SEARCH_ENDPOINT, path)
    response = requests.get(endpoint, headers=BING_HEADERS, params=params)
    items = response.json()
    return items


def find_information(query, market="en-US"):
    """Find information using the Bing Search API"""
    params = {"q": query, "mkt": market, "count": 5}
    items = _make_request("v7.0/search", params)
    log_output(items)
    pages = [
        {"url": a["url"], "name": a["name"], "description": a["snippet"]}
        for a in items["webPages"]["value"]
    ]
    related = [a["text"] for a in items["relatedSearches"]["value"]]
    return {"pages": pages, "related": related}


def find_entities(query, market="en-US"):
    """Find entities using the Bing Entity Search API"""
    params = "?mkt=" + market + "&q=" + urllib.parse.quote(query)
    items = _make_request(f"v7.0/entities{params}")
    entities = []
    if "entities" in items:
        entities = [
            {"name": e["name"], "description": e["description"]}
            for e in items["entities"]["value"]
        ]
    return entities

def find_news(query, market="en-US"):
    """Find images using the Bing News Search API"""
    params = {"q": query, "mkt": market, "count": 5}
    items = _make_request("v7.0/news/search", params)
    articles = [
        {
            "name": a["name"],
            "url": a["url"],
            "description": a["description"],
            "provider": a["provider"][0]["name"],
            "datePublished": a["datePublished"],
        }
        for a in items["value"]
    ]
    return articles

@trace
def execute(request: str, instructions: str, feedback: str = ""):
    """Assign a research task to a researcher"""
    functions = {
        "find_information": find_information,
        "find_entities": find_entities,
        "find_news": find_news,
    }

    # create path to prompty file
    configuration = AzureOpenAIModelConfiguration(
        azure_deployment=os.getenv("AZURE_OPENAI_35_TURBO_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    override_model = {
        "configuration": configuration,
        "parameters": {"max_tokens": 512}
    }
    prompty_obj = Prompty.load(folder + "/researcher.prompty", model=override_model)
    results = prompty_obj(request=request, instructions=instructions, feedback=feedback)

    research = []
    for tool in results['tool_calls']:
        if 'function' not in tool:
            continue

        fn = tool['function']
        args = json.loads(fn['arguments'])
        r = functions[fn['name']](**args)
        research.append(
            {"id": tool['id'], "function": fn['name'], "arguments": args, "result": r}
        )

    return research


def process(research):
    """Process the research results"""
    # process web searches
    web = filter(lambda r: r["function"] == "find_information", research)
    web_items = [page for web_item in web for page in web_item["result"]["pages"]]

    # process entity searches
    entities = filter(lambda r: r["function"] == "find_entities", research)
    entity_items = [
        {"url": "None Available", "name": it["name"], "description": it["description"]}
        for e in entities
        for it in e["result"]
    ]

    # process news searches
    news = filter(lambda r: r["function"] == "find_news", research)
    news_items = [
        {
            "url": article["url"],
            "name": article["name"],
            "description": article["description"],
        }
        for news_item in news
        for article in news_item["result"]
    ]
    return {
        "web": web_items,
        "entities": entity_items,
        "news": news_items,
    }


def research(request, instructions, feedback: str = ""):
    r = execute(request=request, instructions=instructions, feedback=feedback)
    p = process(r)
    return p


if __name__ == "__main__":
    # Get command line arguments

    #context = "Can you find the latest camping trends and what folks are doing in the winter?"
    context = sys.argv[1]
    instructions = sys.argv[2]

    r = execute(context=context, instructions=instructions, feedback="")
    processed = process(r)
    print(json.dumps(processed, indent=2))
