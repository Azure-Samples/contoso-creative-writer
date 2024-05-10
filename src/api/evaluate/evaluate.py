# https://github.com/Azure-Samples/contoso-chat/blob/may-2024-updates/evaluations/evaluate-chat-flow-sdk.ipynb
import os
from datetime import datetime
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluators import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator
from promptflow.evals.evaluate import evaluate
from dotenv import load_dotenv

load_dotenv()

# Initialize Azure OpenAI Connection
model_config = AzureOpenAIModelConfiguration(
        azure_deployment="gpt-4",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
    )

# create unique id for each run with date and time
run_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
run_id = f"{run_prefix}_chat_evaluation_sdk"    
print(run_id)

# import sys
# sys.path.append('../contoso_chat')  # Replace '/path/to/contoso_chat' with the actual path to the 'contoso_chat' folder

eval_result = evaluate(
    evaluation_name=run_id,
    data="eval_data.jsonl",
    evaluators={
        #"violence": violence_eval,
        "relevance": RelevanceEvaluator(model_config),
        "fluency": FluencyEvaluator(model_config),
        "coherence": CoherenceEvaluator(model_config),
        "groundedness": GroundednessEvaluator(model_config),
    },
    # column mapping    return {"question": question, "answer": result, "context": context}
    evaluator_config={
        "defaults": {
            "question": "${data.question}",
            "answer": "${data.answer}",
            "context": "${data.context}",
        },
    },
)

#save evaluation results to a JSONL file
eval_result.to_json('eval_result.jsonl', orient='records', lines=True)
