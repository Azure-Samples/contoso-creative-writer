import os
import json
import logging
import prompty
from opentelemetry import trace
from opentelemetry.trace import set_span_in_context
from azure.ai.evaluation import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator, ContentSafetyEvaluator
from azure.ai.evaluation import ViolenceEvaluator, HateUnfairnessEvaluator, SelfHarmEvaluator, SexualEvaluator
from azure.ai.evaluation import evaluate

from azure.identity import DefaultAzureCredential

logging.getLogger('promptflow.core._prompty_utils').setLevel(logging.CRITICAL)

class FriendlinessEvaluator:
    def __init__(self) -> None:
        pass

    def __call__(self, response):
        model_config = {
            "azure_deployment": os.environ.get("AZURE_OPENAI_4_EVAL_DEPLOYMENT_NAME"),
            "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT")
        }
        result = prompty.execute(
            "friendliness.prompty",
            configuration=model_config,
            inputs={
                "response": response,
            }
        )
        return {"score": result}

class ArticleEvaluator:
    def __init__(self, model_config, project_scope):
        self.evaluators = {
            "relevance": RelevanceEvaluator(model_config),
            "fluency": FluencyEvaluator(model_config),
            "coherence": CoherenceEvaluator(model_config),
            "groundedness": GroundednessEvaluator(model_config),
            "violence": ViolenceEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            "hate-unfairness": HateUnfairnessEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            "self-harm": SelfHarmEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            "sexual": SexualEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            "friendliness": FriendlinessEvaluator(),
        }
        self.project_scope = project_scope

    def __call__(self, *, data_path, **kwargs):
        output = {}
        ## NOTE: - The following code expects that the user has Storage Blob Data Contributor permissions in order for the results to upload to the Azure AI Studio.
        result = evaluate(
            data=data_path,
            evaluators=self.evaluators,
            ## NOTE: If you do not have Storage Blob Data Contributor permissions, please comment out the below line of code. 
            azure_ai_project=self.project_scope,
            evaluator_config={
                "relevance": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "fluency": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "coherence": {
                        "column_mapping": {
                        "response": "${data.response}",
                        "query": "${data.query}",
                    },
                },
                "groundedness": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "violence": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "self-harm": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "hate-unfairness": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "sexual": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "friendliness": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
            },
        )
        output.update(result)
        return output
    
def evaluate_article(data, trace_context):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("run_evaluators", context=trace_context) as span:
        span.set_attribute("inputs", json.dumps(data))
        configuration = {
            "azure_deployment": os.environ["AZURE_OPENAI_4_EVAL_DEPLOYMENT_NAME"],   
            "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
            "azure_endpoint": f"https://{os.getenv('AZURE_OPENAI_NAME')}.cognitiveservices.azure.com/"
        }
        project_scope = {
            "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],   
            "resource_group_name": os.environ["AZURE_RESOURCE_GROUP"],
            "project_name": os.environ["AZURE_AI_PROJECT_NAME"],        
        }
        evaluator = ArticleEvaluator(configuration, project_scope)
        results = evaluator(data)
        resultsJson = json.dumps(results)
        span.set_attribute("output", resultsJson)

        print("results: ", resultsJson)

def evaluate_article_in_background(research_context, product_context, assignment_context, research, products, article):
    eval_data = {
        "query": json.dumps({
            "research_context": research_context,
            "product_context": product_context,
            "assignment_context": assignment_context
        }),
        "context": json.dumps({
            "research": research,
            "products": products,
        }),
        "response": json.dumps(article)
    }

    # propagate trace context to the new thread
    span = trace.get_current_span()
    trace_context = set_span_in_context(span)
   
    evaluate_article(eval_data, trace_context)
   
