import json
import os
import prompty
import requests
import sys
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

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


@prompty.trace
def find_information(query, market="en-US"):
    """Find information using the Bing Search API"""
    params = {"q": query, "mkt": market, "count": 5}
    items = _make_request("v7.0/search", params)
    pages = [
        {"url": a["url"], "name": a["name"], "description": a["snippet"]}
        for a in items["webPages"]["value"]
    ]
    related = [a["text"] for a in items["relatedSearches"]["value"]]
    return {"pages": pages, "related": related}


@prompty.trace
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


@prompty.trace
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


@prompty.trace
def research(context: str, instructions: str, feedback: str = "", tools=[]):
    """Assign a research task to a researcher"""
    functions = {
        "find_information": find_information,
        "find_entities": find_entities,
        "find_news": find_news,
    }
    fns = prompty.execute(
        "researcher.prompty",
        inputs={
            "context": context,
            "instructions": instructions,
            "feedback": feedback,
            "tools": tools,
        },
    )
    research = []
    for f in fns:
        fn = functions[f.name]
        args = json.loads(f.arguments)
        r = fn(**args)
        research.append(
            {"id": f.id, "function": f.name, "arguments": args, "result": r}
        )

    return research


@prompty.trace
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


if __name__ == "__main__":
    # Get command line arguments
    if len(sys.argv) < 3:
        context = "I want to write an article about Satya Nadella and the beginnings of his career."
        instructions = "Can you find the relevant information on both him as a person and what he studied and maybe some news articles?"
    else:
        context = sys.argv[0]
        instructions = sys.argv[1]

    r = research(context=context, instructions=instructions)
    processed = process(r)
    print(json.dumps(processed, indent=2))
