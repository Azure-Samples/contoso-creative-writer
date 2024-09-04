import os
import json
from pathlib import Path
import prompty
from prompty.tracer import trace
from dotenv import load_dotenv
    
load_dotenv()

import prompty.azure
from prompty.tracer import trace, Tracer, PromptyTracer
 
json_tracer = PromptyTracer(output_dir=".")
Tracer.add("PromptyTracer", json_tracer.tracer)
 
@trace

def evaluate_friendliness(response : str):

    model_config = {
        "azure_deployment": os.environ.get("AZURE_OPENAI_4_EVAL_DEPLOYMENT_NAME"),
        "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT")
    }

    print(model_config)
    
    result = prompty.execute(
        "friendliness.prompty",
        configuration = model_config,
        inputs = {
            "response": response,
        }   
    )
    return result

if __name__ == "__main__":

    result = evaluate_friendliness("I am happy to help you with that.")
    print(result)
