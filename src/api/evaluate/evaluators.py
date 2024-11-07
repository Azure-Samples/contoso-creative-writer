import os
import json
import logging

from opentelemetry import trace
from opentelemetry.trace import set_span_in_context
from azure.ai.evaluation import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator, ContentSafetyEvaluator
from azure.ai.evaluation import evaluate, ViolenceEvaluator, HateUnfairnessEvaluator, SelfHarmEvaluator, SexualEvaluator, ContentSafetyMultimodalEvaluator
from azure.ai.evaluation import ViolenceMultimodalEvaluator
from azure.identity import DefaultAzureCredential

logging.getLogger('promptflow.core._prompty_utils').setLevel(logging.CRITICAL)


class ArticleEvaluator:
    def __init__(self, model_config, project_scope):
        self.evaluators = [
            RelevanceEvaluator(model_config),
            FluencyEvaluator(model_config),
            CoherenceEvaluator(model_config),
            GroundednessEvaluator(model_config),
            ViolenceEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            HateUnfairnessEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            SelfHarmEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential()),
            SexualEvaluator(azure_ai_project=project_scope, credential=DefaultAzureCredential())
        ]

    def __call__(self, *, query: str, context: str, response: str, **kwargs):
        output = {}
        for evaluator in self.evaluators:
            result = evaluator(
                query=query,
                context=context,
                response=response,
            )
            output.update(result)

            if not isinstance(evaluator, ContentSafetyEvaluator):
                print(f"{evaluator._RESULT_KEY} evaluation done!")
            else:
                print(f"Content saftey evaluation in done!")
                
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
        results = evaluator(query=data['query'], context=data['context'], response=data['response'])
        resultsJson = json.dumps(results)
        span.set_attribute("output", resultsJson)

        print("results: ", resultsJson)

def evaluate_image(image_path, project_scope):
    import uuid
    azure_cred = DefaultAzureCredential()
    content_safety_eval = ViolenceMultimodalEvaluator(
        azure_ai_project=project_scope, credential=azure_cred
    )
    # conversation={"conversation":{
    #             "messages": [
    #                 {
    #                     "role": "user",
    #                     "content": [
    #                         {
    #                             "type": "text",
    #                             "text": "Can you describe this image?"
    #                         },
    #                         {
    #                             "type": "image_url",
    #                             "image_url": {
    #                                 "url": "https://cdn.britannica.com/68/178268-050-5B4E7FB6/Tom-Cruise-2013.jpg"
    #                             }
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "role": "system",
    #                     "content": [
    #                         {
    #                             "type": "text",
    #                             "text": "This picture of a man"
    #                         }],
                        
    #                 }
    #             ]
    #         }
    # }
    
    # Specify the JSONL file path
    jsonl_file_path = "conversation_data.jsonl"

    from pprint import pprint

    # # Write conversation to JSONL file
    # with open(jsonl_file_path, "a") as jsonl_file:
    #     json.dump(conversation, jsonl_file)
    #     jsonl_file.write("\n")
    

    #This works as expected but we need to figure out how we can manually add images in. 
    #maybe create an image url. Figure out where I'm going wrong
    result = evaluate(
        evaluation_name=f"evaluate-api-multi-modal-eval-dataset-{str(uuid.uuid4())}",
        azure_ai_project=project_scope,
        data=jsonl_file_path,
        evaluators={"content_safety": content_safety_eval},
        evaluator_config={
            "content_safety": {"conversation": "${data.conversation}"},
        }
    )

    print("\n======= Eval Results ======")
    pprint(result["rows"])
        


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
   