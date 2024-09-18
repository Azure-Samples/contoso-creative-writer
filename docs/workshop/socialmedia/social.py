import os
import sys
import prompty
import prompty.azure
from prompty.tracer import trace, Tracer, PromptyTracer

# Import the researcher agent to use here
sys.path.append(os.path.abspath('../../docs/workshop/researcher/'))
from researcher3 import research

#initiate local prompty tracing
local_trace = PromptyTracer()
Tracer.add("PromptyTracer", local_trace.tracer)

@trace
def execute_social_media_writer_prompty(research_context: str, research, social_media_instructions: str):
    """Create the twitter thread using Prompty"""
    
    reseponse = prompty.execute(
        "social.prompty", inputs={"research_context": research_context, "research": research, "assignment": social_media_instructions}
    )

    return reseponse

def run_social_media_agent(instructions: str, social_media_instructions: str):
    """
    Run the social media agent

    Execute the researcher prompty to find information, entities, and news
    execute the social media writer prompty to create the twitter thread
    """
    research_results = research(instructions)
    thread = execute_social_media_writer_prompty(research_context= instructions, research=research_results, social_media_instructions = social_media_instructions)
    print(thread)
