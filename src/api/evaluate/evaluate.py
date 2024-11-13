# https://github.com/Azure-Samples/contoso-chat/blob/may-2024-updates/evaluations/evaluate-chat-flow-sdk.ipynb
import os
import sys
import json
from pathlib import Path
from .evaluators import ArticleEvaluator, ImageEvaluator
from orchestrator import create
from prompty.tracer import trace
from azure.identity import DefaultAzureCredential
from azure.ai.project import AIProjectClient
from azure.ai.project.models import Evaluation, Dataset, EvaluatorConfiguration, ConnectionType
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from dotenv import load_dotenv

load_dotenv()
folder = Path(__file__).parent.absolute().as_posix()

# # Add the api directory to the sys.path
# sys.path.append(os.path.abspath('../src/api'))


def evaluate_remote(data_path):
    # Create an Azure AI Client from a connection string, copied from your AI Studio project.
    # At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
    # Customer needs to login to Azure subscription via Azure CLI and set the environment variables

    ai_project_conn_str = os.getenv("AZURE_LOCATION")+".api.azureml.ms;"+os.getenv("AZURE_SUBSCRIPTION_ID")+";"+os.getenv("AZURE_RESOURCE_GROUP")+";"+os.getenv("AZURE_AI_PROJECT_NAME")

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=ai_project_conn_str,
    )

    data_id = project_client.upload_file(data_path)

    default_connection = project_client.connections.get_default(connection_type=ConnectionType.AZURE_OPEN_AI)

    deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
    api_version = os.environ["AZURE_OPENAI_API_VERSION"]

    model_config = default_connection.to_evaluator_model_config(deployment_name=deployment_name, api_version=api_version)
    # Create an evaluation
    evaluation = Evaluation(
        display_name="Remote Evaluation",
        description="Evaluation of dataset",
        data=Dataset(id=data_id),
        evaluators={
            "relevance": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Relevance-Evaluator/versions/4",
                init_params={
                    "model_config": model_config
                },
            ),
            "fluency": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Fluency-Evaluator/versions/4",
                init_params={
                    "model_config": model_config
                },
            ),
            "coherence": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Coherence-Evaluator/versions/4",
                init_params={
                    "model_config": model_config
                },
            ),
            "groundedness": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Groundedness-Evaluator/versions/4",
                init_params={
                    "model_config": model_config
                },
            ),
            "violence": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Violent-Content-Evaluator/versions/3",
                init_params={
                    "azure_ai_project": project_client.scope
                },
            ),
            "hate_unfairness": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Hate-and-Unfairness-Evaluator/versions/4",
                init_params={
                    "azure_ai_project": project_client.scope
                },
            ),
            "self_harm": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Self-Harm-Related-Content-Evaluator/versions/3",
                init_params={
                    "azure_ai_project": project_client.scope
                },
            ),
            "sexual": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Sexual-Content-Evaluator/versions/3",
                init_params={
                    "azure_ai_project": project_client.scope
                },
            ),
        },
    )

    # Create evaluation
    evaluation_response = project_client.evaluations.create(
        evaluation=evaluation,
    )
    # Get evaluation
    get_evaluation_response = project_client.evaluations.get(evaluation_response.id)

    print("----------------------------------------------------------------")
    print("Created remote evaluation, evaluation ID: ", get_evaluation_response.id)
    print("Evaluation status: ", get_evaluation_response.status)
    print("AI Studio URI: ", get_evaluation_response.properties["AiStudioEvaluationUri"])
    print("----------------------------------------------------------------")



def run_orchestrator(research_context, product_context, assignment_context):
    query = {"research_context": research_context, "product_context": product_context, "assignment_context": assignment_context}
    context = {}
    response = None

    for result in create(research_context, product_context, assignment_context,evaluate=False):
        if not type(result) == tuple:
            parsed_result = json.loads(result)
        if type(parsed_result) is list:
            if parsed_result[0] == "researcher":
                context['research'] = parsed_result[1]
            if parsed_result[0] == "products":
                context['products'] = parsed_result[1]
            if parsed_result[0] == "writer":
                response = parsed_result[1]
    
    return {
        "query": json.dumps(query), 
        "context": json.dumps(context), 
        "response": json.dumps(response),
    }

@trace
def evaluate_orchestrator(model_config, project_scope,  data_path):
    writer_evaluator = ArticleEvaluator(model_config, project_scope)

    data = []    
    eval_data = []
    print(f"\n===== Creating articles to evaluate using data provided in {data_path}")
    print("")
    with open(data_path) as f:
        for num, line in enumerate(f):
            row = json.loads(line)
            data.append(row)
            print(f"generating article {num +1}")
            eval_data.append(run_orchestrator(row["research_context"], row["product_context"], row["assignment_context"]))

    # write out eval data to a file so we can re-run evaluation on it
    with jsonlines.open(folder + '/eval_data.jsonl', 'w') as writer:
        for row in eval_data:
            writer.write(row)

    eval_data_path = folder + '/eval_data.jsonl'

    print(f"\n===== Evaluating the generated articles")
    eval_results = writer_evaluator(data_path=eval_data_path)
    import pandas as pd

    print("Evaluation summary:\n")
    print("View in Azure AI Studio at: " + str(eval_results['studio_url']))
    metrics = {key: [value] for key, value in eval_results['metrics'].items()}
    results_df = pd.DataFrame.from_dict(metrics)
    results_df_gpt_evals = results_df[['relevance.gpt_relevance', 'fluency.gpt_fluency', 'coherence.gpt_coherence','groundedness.gpt_groundedness']]
    results_df_content_safety = results_df[['violence.violence_defect_rate', 'self_harm.self_harm_defect_rate', 'hate_unfairness.hate_unfairness_defect_rate','sexual.sexual_defect_rate']]

    mean_df = results_df_gpt_evals.mean()
    print("\nAverage scores:")
    print(mean_df)

    content_safety_mean_df = results_df_content_safety.mean()
    print("\nContent safety average defect rate:")
    print(content_safety_mean_df)

    results_df.to_markdown(folder + '/eval_results.md')
    with open(folder + '/eval_results.md', 'a') as file:
        file.write("\n\nAverages scores:\n\n")
    mean_df.to_markdown(folder + '/eval_results.md', 'a')

    with jsonlines.open(folder + '/eval_results.jsonl', 'w') as writer:
        writer.write(eval_results)

    return eval_results

def evaluate_image(project_scope,  image_path):
    image_evaluator = ImageEvaluator(project_scope)

    import pathlib 
    import base64

    import validators
    

    if validators.url(image_path):
        url_path = image_path
    else:
        #encode an image or you can add an image file from a url
        with pathlib.Path(image_path).open("rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            url_path = f"data:image/jpg;base64,{encoded_image}"

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    client = AzureOpenAI(
        azure_endpoint = f"{os.getenv('AZURE_OPENAI_ENDPOINT')}", 
        api_version="2023-07-01-preview",
        azure_ad_token_provider=token_provider
    )

    sys_message = "You are an AI assistant that describes images in details."

    messages = []

    print(f"\n===== URL : [{url_path}]")
    print(f"\n===== Calling Open AI to describe image and retrieve response")
    completion = client.chat.completions.create(
    model="gpt-4-evals",
    messages= [
                    {
                        "role": "system", 
                        "content": [
                            {"type": "text", "text": sys_message}
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Can you describe this image?"},
                            {"type": "image_url", "image_url": {"url": url_path}},
                        ],
                    },
                ],
        )
    
    message = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": sys_message}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Can you describe this image?"},
                    {"type": "image_url", "image_url": {"url": url_path}},
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": completion.choices[0].message.content},
                ],
            },
        ]
    
    messages.append(message)
    print(f"\n===== Evaluating response")
    eval_results = image_evaluator(messages=messages)

    import pandas as pd

    print("Image Evaluation summary:\n")
    print("View in Azure AI Studio at: " + str(eval_results['studio_url']))
    metrics = {key: [value] for key, value in eval_results['metrics'].items()}
    
    results_df = pd.DataFrame.from_dict(metrics)

    result_keys = [*metrics.keys()]
    
    results_df_gpt_evals = results_df[result_keys]

    mean_df = results_df_gpt_evals.mean()
    print("\nAverage scores:")
    print(mean_df)

    results_df.to_markdown(folder + '/image_eval_results.md')
    with open(folder + '/image_eval_results.md', 'a') as file:
        file.write("\n\nAverages scores:\n\n")
    mean_df.to_markdown(folder + '/image_eval_results.md', 'a')

    with jsonlines.open(folder + '/image_eval_results.jsonl', 'w') as writer:
        writer.write(eval_results)

    return eval_results



if __name__ == "__main__":
    import time
    import jsonlines
    import pathlib
    from pprint import pprint
    

    model_config = {
        "azure_deployment":os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],   
        "api_version":os.environ["AZURE_OPENAI_API_VERSION"],
        "azure_endpoint":f"https://{os.getenv('AZURE_OPENAI_NAME')}.cognitiveservices.azure.com/"
    }
    project_scope = {
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],   
        "resource_group_name": os.environ["AZURE_RESOURCE_GROUP"],
        "project_name": os.environ["AZURE_AI_PROJECT_NAME"],        
    }
    
    start=time.time()
    print(f"Starting evaluate...")

    eval_result = evaluate_orchestrator(model_config, project_scope, data_path=folder +"/eval_inputs.jsonl")
    evaluate_remote(data_path=folder +"/eval_data.jsonl")

    #This is code to add an image from a file path
    # parent = pathlib.Path(__file__).parent.resolve()
    # path = os.path.join(parent, "data")
    # image_path = os.path.join(path, "image1.jpg")

    image_path = "https://i.imgflip.com/9a1vlj.jpg"

    eval_image_result = evaluate_image(project_scope, image_path)

    end=time.time()
    print(f"Finished evaluate in {end - start}s")
