# https://github.com/Azure-Samples/contoso-chat/blob/may-2024-updates/evaluations/evaluate-chat-flow-sdk.ipynb
import os
import sys
import json
from pathlib import Path
from .evaluators import ArticleEvaluator
from orchestrator import create
from prompty.tracer import trace
from tracing import init_tracing
from azure.identity import DefaultAzureCredential
from azure.ai.project import AIProjectClient
from azure.ai.project.models import Evaluation, Dataset, EvaluatorConfiguration, ConnectionType
from azure.ai.evaluation import RelevanceEvaluator, FluencyEvaluator, CoherenceEvaluator, GroundednessEvaluator, ViolenceEvaluator, HateUnfairnessEvaluator, SelfHarmEvaluator, SexualEvaluator

from dotenv import load_dotenv

load_dotenv()
folder = Path(__file__).parent.absolute().as_posix()

# # Add the api directory to the sys.path
# sys.path.append(os.path.abspath('../src/api'))


def evaluate_remote(data_path):
    # Create an Azure AI Client from a connection string, copied from your AI Studio project.
    # At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
    # Customer needs to login to Azure subscription via Azure CLI and set the environment variables

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str="eastus2.api.azureml.ms;70e1ee3b-e694-4bce-9bff-d5d982d936d7;rg-ignite-11-7-2;ai-project-ykb63sonpiqqk",
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
            "hateunfairness": EvaluatorConfiguration(
                id="azureml://registries/azureml/models/Hate-and-Unfairness-Evaluator/versions/4",
                init_params={
                    "azure_ai_project": project_client.scope
                },
            ),
            "selfharm": EvaluatorConfiguration(
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
            # "friendliness": EvaluatorConfiguration(
            #     id="azureml://locations/eastus2/workspaces/f41c33c3-0aa4-41d1-bba7-31ce3bdaf0ab/models/blue_stem_7dg00zlwmt/versions/1",
            #     init_params={
            #         "model_config": model_config
            #     }
            # )
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
    with open(data_path) as f:
        for line in f:
            row = json.loads(line)
            data.append(row)
            eval_data.append(run_orchestrator(row["research_context"], row["product_context"], row["assignment_context"]))

    # write out eval data to a file so we can re-run evaluation on it
    with jsonlines.open(folder + '/eval_data.jsonl', 'w') as writer:
        for row in eval_data:
            # print(row)
            writer.write(row)

    eval_data_path = folder + '/eval_data.jsonl'

    eval_results = writer_evaluator(data_path=eval_data_path)
    import pandas as pd

    print("Evaluation summary:\n")
    print("View in Azure AI Studio at: " + str(eval_results['studio_url']))
    metrics = {key: [value] for key, value in eval_results['metrics'].items()}
    results_df = pd.DataFrame.from_dict(metrics)
    results_df_gpt_evals = results_df[['relevance.gpt_relevance', 'fluency.gpt_fluency', 'coherence.gpt_coherence','groundedness.gpt_groundedness']]
    results_df_content_safety = results_df[['violence.violence_defect_rate', 'self-harm.self_harm_defect_rate', 'hate-unfairness.hate_unfairness_defect_rate','sexual.sexual_defect_rate']]

    # mean_df = results_df.drop("research_context", axis=1).mean()
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

if __name__ == "__main__":
    import time
    import jsonlines
    

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
    # print(os.environ["BING_SEARCH_ENDPOINT"])
    # print("value: ", os.environ["BING_SEARCH_KEY"], len(os.environ["BING_SEARCH_KEY"]))


    tracer = init_tracing(local_tracing=True)

    eval_result = evaluate_orchestrator(model_config, project_scope, data_path=folder +"/eval_inputs.jsonl")
    evaluate_remote(data_path=folder +"/eval_data.jsonl")

    end=time.time()
    print(f"Finished evaluate in {end - start}s")