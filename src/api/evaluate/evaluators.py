import os
import json
import logging
import prompty
from opentelemetry import trace
from opentelemetry.trace import set_span_in_context
from azure.ai.evaluation import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator
from azure.ai.evaluation import ViolenceEvaluator, HateUnfairnessEvaluator, SelfHarmEvaluator, SexualEvaluator
from azure.ai.evaluation import evaluate
from azure.ai.evaluation import ViolenceMultimodalEvaluator, SelfHarmMultimodalEvaluator, HateUnfairnessMultimodalEvaluator, SexualMultimodalEvaluator
from azure.ai.evaluation import ContentSafetyMultimodalEvaluator, ProtectedMaterialMultimodalEvaluator
from azure.identity import DefaultAzureCredential


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
            "hate_unfairness": HateUnfairnessEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            "self_harm": SelfHarmEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
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
            # azure_ai_project=self.project_scope,
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
                "self_harm": {
                    "column_mapping": {
                        "response": "${data.response}",
                        "context": "${data.context}",
                        "query": "${data.query}",
                    },
                },
                "hate_unfairness": {
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
    
class ImageEvaluator:
    def __init__(self, project_scope):
        self.evaluators = {
             "content_safety": ContentSafetyMultimodalEvaluator(credential=DefaultAzureCredential(), azure_ai_project=project_scope), 
            "protected_material": ProtectedMaterialMultimodalEvaluator(credential=DefaultAzureCredential(), azure_ai_project=project_scope)
        }
        self.project_scope = project_scope


    def __call__(self, *, messages, **kwargs): 
        import uuid
        import pathlib
        from pprint import pprint
        import pandas as pd

        file_name="dataset_images.jsonl"    
        parent = pathlib.Path(__file__).parent.resolve()
        path = os.path.join(parent, "data")
        datafile_jsonl_path = os.path.join(path, file_name)
        with open(datafile_jsonl_path, "w") as outfile:
            for message in messages:
                conversation = {"conversation": { "messages" : message}}
                json_line = json.dumps(conversation)
                outfile.write(json_line + "\n")

        print("\n===== Reading Data File =======")

        data_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "data")
        file_path = os.path.join(data_path, file_name)
        input_data = pd.read_json(file_path, lines=True)
        pprint(input_data)


        print("\n===== Calling Evaluate API - Content Safety & Protected Material Evaluator for multi-modal =======")
        output = {}
        result = evaluate(
            evaluation_name=f"evaluate-api-multi-modal-eval-dataset-{str(uuid.uuid4())}",
            data=file_path,
            evaluators=self.evaluators,
            azure_ai_project=self.project_scope,
            evaluator_config={
                "content_safety": {"conversation": "${data.conversation}"}, 
                "protected_material": {"conversation": "${data.conversation}"} 
            }
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

def evaluate_image(messages):
    # tracer = trace.get_tracer(__name__)
    # with tracer.start_as_current_span("run_image_evaluators", context=trace_context) as span:
    #     span.set_attribute("inputs", json.dumps(conversation))
    project_scope = {
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],   
        "resource_group_name": os.environ["AZURE_RESOURCE_GROUP"],
        "project_name": os.environ["AZURE_AI_PROJECT_NAME"],        
    }
    evaluator = ImageEvaluator(project_scope)
    results = evaluator(messages)
    resultsJson = json.dumps(results)

    print("results: ", resultsJson)


   
