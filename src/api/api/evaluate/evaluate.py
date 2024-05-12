# https://github.com/Azure-Samples/contoso-chat/blob/may-2024-updates/evaluations/evaluate-chat-flow-sdk.ipynb
import os
import json
from datetime import datetime
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluate import evaluate
from api.evaluate.writer import WriterEvaluator

from dotenv import load_dotenv

load_dotenv()

def evaluate_aistudio(model_config, data_path):
    # create unique id for each run with date and time
    run_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
    run_id = f"{run_prefix}_chat_evaluation_sdk"    
    print(run_id)

    result = evaluate(
        evaluation_name=run_id,
        data=data_path,
        evaluators={
            "writer": WriterEvaluator(model_config),
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

def evaluate_local(model_config, data_path):
    data = []
    with open(data_path) as f:
        for line in f:
            data.append(json.loads(line))

    writer_evaluator = WriterEvaluator(model_config)

    results = []
    futures = []
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for row in data:
            futures.append(executor.submit(writer_evaluator, query=row["query"], context=row["context"], response=row["response"]))
        for future in futures:
            results.append(future.result())

    return results

if __name__ == "__main__":
    import time
    import jsonlines

    # Initialize Azure OpenAI Connection
    model_config = AzureOpenAIModelConfiguration(
            azure_deployment=os.environ["AZURE_DEPLOYMENT_NAME"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
        )

    start=time.time()
    print(f"Starting evaluate...")

    eval_result = evaluate_aistudio(model_config, data_path="api/evaluate/eval_writer.jsonl")

    end=time.time()
    print(f"Finished evaluate in {end - start}s")

    #save evaluation results to a JSONL file
    with jsonlines.open('eval_writer_result.jsonl', 'w') as writer:
        writer.write(eval_result)
