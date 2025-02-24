import os
import sys
import json
from dotenv import load_dotenv
import prompty
import time
import prompty.azure
from prompty.azure.processor import ToolCall
from prompty.tracer import trace
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import BingGroundingTool
from azure.ai.inference.prompts import PromptTemplate
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_result

load_dotenv()

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables


@trace
def execute_research(instructions: str, feedback: str = "No feedback"):

    ai_project_conn_str = os.getenv("AZURE_LOCATION")+".api.azureml.ms;"+os.getenv("AZURE_SUBSCRIPTION_ID")+";"+os.getenv("AZURE_RESOURCE_GROUP")+";"+os.getenv("AZURE_AI_PROJECT_NAME")

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=ai_project_conn_str,
    )

    prompt_template = PromptTemplate.from_prompty(file_path="researcher.prompty")


    instructions = instructions
    feedback= feedback
    messages = prompt_template.create_messages(instructions=instructions, feedback=feedback)

    bing_connection = project_client.connections.get(
        connection_name='bing-connection'
    )
    conn_id = bing_connection.id

    # Initialize agent bing tool and add the connection id
    bing = BingGroundingTool(connection_id=conn_id)

    prompt_template = PromptTemplate.from_prompty(file_path="researcher.prompty")

    # Create agent with the bing tool and process assistant run
    with project_client:
        agent = project_client.agents.create_agent(
            model="gpt-4",
            name="my-assistant",
            instructions=messages[0]['content'],
            tools=bing.definitions,
        )

        print(f"Created agent, ID: {agent.id}")

        # Create thread for communication
        thread = project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")

        # Create message to thread
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=instructions,
        )
        print(f"Created message, ID: {message.id}")

        # # Create and process agent run in thread with tools
        # run = project_client.agents.create_stream(thread_id=thread.id, assistant_id=agent.id)
        def is_rate_limited(run):
            # Check if the run failed due to rate limit
            if run.status == "failed" and run.last_error and run.last_error.get('code') == 'rate_limit_exceeded':
                print(f"Run failed: {run.last_error}")
                return True  # Indicates Tenacity should retry
            return False  # No retry needed

        @retry(
            retry=retry_if_result(is_rate_limited),
            wait=wait_exponential(multiplier=1, min=4, max=60),
            stop=stop_after_attempt(6)
        )
        def run_agent():
        # Create and process agent run in thread with tools
            run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
            print(f"Run finished with status: {run.status}")
            return run
        
        run = run_agent()
        # Retrieve run step details to get Bing Search query link
        # To render the webpage, we recommend you replace the endpoint of Bing search query URLs with `www.bing.com` and your Bing search query URL would look like "https://www.bing.com/search?q={search query}"
        run_steps = project_client.agents.list_run_steps(run_id=run.id, thread_id=thread.id)
        run_steps_data = run_steps['data']

        print(f"Agent created and now researching...")
        print('')

        # Delete the assistant when done
        project_client.agents.delete_agent(agent.id)

        # Fetch and log all messages
        messages = project_client.agents.list_messages(thread_id=thread.id)
        # print(f"Messages: {messages}")
        research_response = messages.data[0]['content'][0]['text']['value']
        try: 
            json_r = json.loads(research_response)
        except:
            print('retrying')
            research_response = messages.data[0]['content'][0]['text']['value']
            json_r = json.loads(research_response)
        research = json_r['web']
        print('research succesfully completed')
        return research

@trace
def research(instructions: str, feedback: str = "No feedback"):
    r = execute_research(instructions=instructions)
    research = {
        "web": r,
        "entities": [],
        "news": [],
    }
    return research


if __name__ == "__main__":
    # Get command line arguments
    if len(sys.argv) < 2:
        instructions = "Can you find the latest camping trends and what folks are doing in the winter?"
    else:
        instructions = sys.argv[1]

    research = execute_research(instructions=instructions)
    # processed = process(r)
    print(json.dumps(research, indent=2))