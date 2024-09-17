import os
import sys
import json
from typing import List
import requests
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv
import prompty
import prompty.azure
from prompty.azure.processor import ToolCall
from prompty.tracer import trace

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



def execute_researcher_prompty(instructions: str, feedback: str = "No feedback"):
    """Assign a research task to a researcher"""
    functions = {
        "find_information": find_information,
        "find_entities": find_entities,
        "find_news": find_news,
    }

    fns: List[ToolCall] = prompty.execute(
        "researcher.prompty", inputs={"instructions": instructions, "feedback": feedback}
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



def extract_findings(research):
    """Extract the research results"""
    # extract web findings
    web = filter(lambda r: r["function"] == "find_information", research)
    web_items = [page for web_item in web for page in web_item["result"]["pages"]]

    # extract entity findings
    entities = filter(lambda r: r["function"] == "find_entities", research)
    entity_items = [
        {"url": "None Available", "name": it["name"], "description": it["description"]}
        for e in entities
        for it in e["result"]
    ]

    # extract news findings
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


def research(instructions: str, feedback: str = "No feedback"):
    """
    Run the research process

    Execute the researcher prompty to find information, entities, and news
    Then extract the findings
    """
    r = execute_researcher_prompty(instructions=instructions)
    p = extract_findings(r)
    return p


def execute_social_media_writer_prompty(research_context: str, research, social_media_instructions: str):
    """Create the twitter thread"""
    
    reseponse = prompty.execute(
        "social.prompty", inputs={"research_context": research_context, "research": research, "assignment": social_media_instructions}
    )

    return reseponse

def run_social_media_agent(instructions: str, social_media_instructions: str):
    """
    Run the social media agent

    Execute the researcher prompty to find information, entities, and news
    Then extract the findings
    And finally execute the social media writer prompty to create the twitter thread
    """
    r = execute_researcher_prompty(instructions=instructions)
    processed = extract_findings(r)
    thread = execute_social_media_writer_prompty(research_context= instructions, research=processed, social_media_instructions = social_media_instructions)
    print(thread)
