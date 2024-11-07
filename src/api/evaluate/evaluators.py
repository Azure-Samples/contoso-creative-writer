import os
import json
import logging

from opentelemetry import trace
from opentelemetry.trace import set_span_in_context
from azure.ai.evaluation import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator, ContentSafetyEvaluator
from azure.ai.evaluation import ViolenceEvaluator, HateUnfairnessEvaluator, SelfHarmEvaluator, SexualEvaluator

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData, ImageCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

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

def evaluate_image(image_path):
    # endpoint = os.environ.get('CONTENT_SAFETY_ENDPOINT')
    # key = os.environ.get('CONTENT_SAFETY_KEY')
    endpoint = "https://safety-ig.cognitiveservices.azure.com/"
    image_path = image_path
    key="D4VBpl18BMX6FxSpm8TLVzISU2L58k3E8WBLDW6HcLOslLYLKSt3JQQJ99AKACfhMk5XJ3w3AAAHACOGGDob"

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))


    # Build request
    with open(image_path, "rb") as file:
        request = AnalyzeImageOptions(image=ImageData(content=file.read()))

    # Analyze image
    try:
        response = client.analyze_image(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == ImageCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == ImageCategory.VIOLENCE)

    results = [hate_result, self_harm_result, sexual_result, violence_result]

    if hate_result:
        print(f"Hate severity: {hate_result.severity}")
    if self_harm_result:
        print(f"SelfHarm severity: {self_harm_result.severity}")
    if sexual_result:
        print(f"Sexual severity: {sexual_result.severity}")
    if violence_result:
        print(f"Violence severity: {violence_result.severity}")

    unsafe_content = []

    for result in results:
        if result.severity > 0:
            unsafe_content.append({f"{result}": result.severity})
    
    if len(unsafe_content) > 0:
            return f"This image cannot be uploaded. It contains the following unsafe content and it's severity level {unsafe_content}."
    else:
        return "Image is safe to upload"


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
   