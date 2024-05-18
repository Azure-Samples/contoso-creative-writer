from promptflow.core import Flow, Prompty, AzureOpenAIModelConfiguration
import os
from dotenv import load_dotenv

load_dotenv()

def design(request, instructions, feedback):
    # Load prompty with AzureOpenAIModelConfiguration override
    configuration = AzureOpenAIModelConfiguration(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    override_model = {
        "configuration": configuration,
        "parameters": {"max_tokens": 512}
    }

    prompty_obj = Prompty.load(
        "editor.prompty", model=override_model)
    
    result = prompty_obj(
        context=request,
        instructions=instructions,
        feedback=feedback,
    )

    return result

if __name__ == "__main__":
    result = design(
        "The request for the designer.",
        "The instructions for the designer.",
        "The feedback for the designer.")
    print(result)
