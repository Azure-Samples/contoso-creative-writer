import os
import json
import sys
sys.path.append(os.path.abspath('../../../src/api/agents/researcher'))
from researcher import execute_research
from typing import List
from dotenv import load_dotenv
import prompty
import prompty.azure
from prompty.azure.processor import ToolCall

load_dotenv()

global_prompty_file_path=os.getcwd()+'/researcher-2.prompty'

def find_information(query, market='en-US'):
    # You can use another api to find information, here we are using "Grounding with Bing Search"
    print("Executing 'Find Information' ToolCall in %s.." % market)
    return execute_research(instructions=query, return_raw=True, prompty_file_path=global_prompty_file_path)

def find_entities(query, market='en-US'):
    # You can use another api to find entities, here we are using "Grounding with Bing Search"
    print("Executing 'Find Entities' ToolCall in %s.." % market)
    return execute_research(instructions=query, return_raw=True, prompty_file_path=global_prompty_file_path)

def find_news(query, market='en-US'):
    print("Executing 'Find News' ToolCall in %s.." % market)
    # You can use another api to find bews, here we are using "Grounding with Bing Search"
    return execute_research(instructions=query, return_raw=True, prompty_file_path=global_prompty_file_path)

def execute_researcher_prompty(instructions: str, prompty_file_path=global_prompty_file_path):
    """
    Executes the researcher prompty to find information, entities, and news,
    and runs the selected function given the query and returns the results
    """

    # Execute the researcher prompty
    function_calls: List[ToolCall] = prompty.execute(
        prompty_file_path, inputs={"instructions": instructions}
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


def research(instructions: str, prompty_file_path: str = None):
    """
    Calls the execute and process functions above to run the research agent 
    and return the results to the user in a readable format. 
    """
    
    global global_prompty_file_path
    if prompty_file_path is not None:
        global_prompty_file_path=prompty_file_path
    function_calls = execute_researcher_prompty(instructions=instructions, prompty_file_path=global_prompty_file_path)
    research = execute_function_calls(function_calls)
    #findings = extract_findings(research)
    return research