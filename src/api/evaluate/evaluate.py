# https://github.com/Azure-Samples/contoso-chat/blob/may-2024-updates/evaluations/evaluate-chat-flow-sdk.ipynb
import os
import sys
import json
import concurrent.futures
from pathlib import Path
from datetime import datetime
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluate import evaluate
from evaluate.evaluators import ArticleEvaluator
from orchestrator import create
from prompty.tracer import trace
from tracing import init_tracing

from dotenv import load_dotenv

load_dotenv()
folder = Path(__file__).parent.absolute().as_posix()

# # Add the api directory to the sys.path
# sys.path.append(os.path.abspath('../src/api'))

def evaluate_aistudio(model_config, data_path):
    # create unique id for each run with date and time
    run_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
    run_id = f"{run_prefix}_chat_evaluation_sdk"    
    print(run_id)

    result = evaluate(
        evaluation_name=run_id,
        data=data_path,
        evaluators={
            "article": ArticleEvaluator(model_config),
        },
        evaluator_config={
            "defaults": {
                "query": "${data.query}",
                "response": "${data.response}",
                "context": "${data.context}",
            },
        },
    )
    return result

def evaluate_data(model_config, data_path):
    writer_evaluator = ArticleEvaluator(model_config)

    data = []
    with open(data_path) as f:
        for line in f:
            data.append(json.loads(line))

    results = []
    for row in data:
        result = writer_evaluator(query=row["query"], context=row["context"], response=row["response"])
        print("Evaluation results: ", result)
        results.append(result)

    return results

def run_orchestrator(research_context, product_context, assignment_context):
    query = {"research_context": research_context, "product_context": product_context, "assignment_context": assignment_context}
    context = {}
    response = None

    for result in create(research_context, product_context, assignment_context):
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
def evaluate_orchestrator(model_config, data_path):
    writer_evaluator = ArticleEvaluator(model_config)

    data = []
    with open(data_path) as f:
        for line in f:
            data.append(json.loads(line))

    eval_data = []
    eval_results = []

    results = []
    # futures = []
    def evaluate_row(research_context, product_context, assignment_context):
        result = { "research_context": research_context }
        print("Running orchestrator...")
        eval_data = run_orchestrator(research_context, product_context, assignment_context)
        print("Evaluating results...")
        eval_result = writer_evaluator(query=eval_data["query"], context=eval_data["context"], response=eval_data["response"])
        result.update(eval_result)
        print("Evaluation results: ", eval_result)
        eval_results.append(result)

    #can not execute concurrently with streamed data because of rate errors 
    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    for row in data:
        results.append(evaluate_row(row["research_context"], row["product_context"], row["assignment_context"]))
        # futures.append(executor.submit(evaluate_row, row["research_context"], row["product_context"], row["assignment_context"]))
    # for future in futures:
        # results.append(future.result())

    # write out eval data to a file so we can re-run evaluation on it
    with jsonlines.open(folder + '/eval_data.jsonl', 'w') as writer:
        for row in eval_data:
            writer.write(row)

    import pandas as pd

    print("Evaluation summary:\n")
    results_df = pd.DataFrame.from_dict(eval_results)
    print(results_df)

    mean_df = results_df.drop("research_context", axis=1).mean()
    print("\nAverage scores:")
    print(mean_df)

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
    
    # Initialize Azure OpenAI Connection
    model_config = AzureOpenAIModelConfiguration(
        azure_deployment=os.environ["AZURE_OPENAI_4_EVAL_DEPLOYMENT_NAME"],   
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_NAME')}.cognitiveservices.azure.com/"
    )

    start=time.time()
    print(f"Starting evaluate...")
    print(os.environ["BING_SEARCH_ENDPOINT"])
    print("value: ", os.environ["BING_SEARCH_KEY"], len(os.environ["BING_SEARCH_KEY"]))


    tracer = init_tracing(local_tracing=True)

    eval_result = evaluate_orchestrator(model_config, data_path=folder +"/eval_inputs.jsonl")

    end=time.time()
    print(f"Finished evaluate in {end - start}s")
