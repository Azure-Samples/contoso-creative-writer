import os
import json
from typing import List
import requests
import urllib.parse
from dotenv import load_dotenv
import prompty
import prompty.azure
from prompty.azure.processor import ToolCall

load_dotenv()

BING_SEARCH_ENDPOINT = os.getenv("BING_SEARCH_ENDPOINT")
BING_SEARCH_KEY = os.getenv("BING_SEARCH_KEY")
BING_HEADERS = {"Ocp-Apim-Subscription-Key": BING_SEARCH_KEY}


def _make_bing_endpoint(endpoint, path):
    """Make a Bing endpoint URL"""
    return f"{endpoint}{'' if endpoint.endswith('/') else '/'}{path}"


def _make_bing_request(path, params=None):
    """Make a request to the Bing API"""
    endpoint = _make_bing_endpoint(BING_SEARCH_ENDPOINT, path)
    response = requests.get(endpoint, headers=BING_HEADERS, params=params)
    items = response.json()
    return items


def find_information(query, market="en-US"):
    """Find information using the Bing Search API"""
    params = {"q": query, "mkt": market, "count": 5}
    items = _make_bing_request("v7.0/search", params)
    pages = [
        {"url": a["url"], "name": a["name"], "description": a["snippet"]}
        for a in items["webPages"]["value"]
    ]
    related = [a["text"] for a in items["relatedSearches"]["value"]]
    return {"pages": pages, "related": related}



def find_entities(query, market="en-US"):
    """Find entities using the Bing Entity Search API"""
    params = "?mkt=" + market + "&q=" + urllib.parse.quote(query)
    items = _make_bing_request(f"v7.0/entities{params}")
    entities = []
    if "entities" in items:
        entities = [
            {"name": e["name"], "description": e["description"]}
            for e in items["entities"]["value"]
        ]
    return entities



def find_news(query, market="en-US"):
    """Find news using the Bing News Search API"""
    params = {"q": query, "mkt": market, "count": 5}
    items = _make_bing_request("v7.0/news/search", params)
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


def execute_researcher_prompty(instructions: str):
    """
    Executes the researcher prompty to find information, entities, and news,
    and runs the selected function given the query and returns the results
    """

    # Execute the researcher prompty
    function_calls: List[ToolCall] = prompty.execute(
        "researcher-2.prompty", inputs={"instructions": instructions}
    )

    return function_calls

def execute_function_calls(function_calls):
    """
    Executes the function calls and returns the results
    """

    # Define the registry of functions that can be called
    functions = {
        "find_information": find_information,
        "find_entities": find_entities,
        "find_news": find_news,
    }

    research = []
    for function_call in function_calls:

        # Resolve function by its name
        function = functions[function_call.name]

        # Parse the arguments
        args = json.loads(function_call.arguments)

        # Execute the function call
        r = function(**args)

        # Append the results to the research list
        research.append(
            {"id": function_call.id, "function": function_call.name, "arguments": args, "result": r}
        )

    return research


def extract_findings(research):
    """
    Extract the research results.
    This function makes the returned results readable
    """
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


def research(instructions: str):
    """
    Calls the execute and process functions above to run the research agent 
    and return the results to the user in a readable format. 
    """

    function_calls = execute_researcher_prompty(instructions=instructions)
    research = execute_function_calls(function_calls)
    findings = extract_findings(research)
    return findings
