import sys
import json
import os
from promptflow.core import Flow, Prompty, AzureOpenAIModelConfiguration

from dotenv import load_dotenv

load_dotenv()

def write(context, feedback, instructions, research = []):
    loaded_prompty = Flow.load("writer.prompty")
    result = loaded_prompty(
        context=context,
        feedback=feedback,
        instructions=instructions,
        research=research,
    )

    # Load prompty with AzureOpenAIModelConfiguration override
    configuration = AzureOpenAIModelConfiguration(
        azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    override_model = {
        "configuration": configuration,
        "parameters": {"max_tokens": 512}
    }

    prompty_obj = Prompty.load(
        "writer.prompty", model=override_model)
    
    result = prompty_obj(
        context=context,
        feedback=feedback,
        instructions=instructions,
        research=research,
    )

    return result

def process(writer):
    # parse string this chracter --- , artcile and feedback
    result = writer.split("---")
    article = str(result[0]).strip()
    if len(result) > 1:
        feedback = str(result[1]).strip()
    else:
        feedback = "No Feedback"

    return {
        "context": {
            "article": article,
            "feedback": feedback,
        }
    }
if __name__ == "__main__":
    # get args from the user
    # check if args if null default to a value
    # if len(sys.argv) == 0:
    #     context="I want to write an article about Satya Nadella and the beginnings of his career.",
    #     feedback="No Feedback",
    #     instructions="Can you help me find information about Satya Nadella's career and beginnings?"
    #     research = []
    # else:
    context = sys.argv[1]
    feedback = sys.argv[2]
    instructions = sys.argv[3]
    research = json.dumps(sys.argv[4])
    result = write(
        context=str(context),
        feedback=str(feedback),
        instructions=str(instructions),
        research=research,
    )
    processed = process(result)
    print(processed)
