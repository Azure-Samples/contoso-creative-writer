import os
import json
from threading import Thread
from opentelemetry import trace
from opentelemetry.trace import set_span_in_context
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluators import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator


class ArticleEvaluator:
    def __init__(self, model_config):
        self.evaluators = [
            RelevanceEvaluator(model_config),
            FluencyEvaluator(model_config),
            CoherenceEvaluator(model_config),
            GroundednessEvaluator(model_config),
        ]

    def __call__(self, *, query: str, context: str, response: str, **kwargs):
        output = {}
        for evaluator in self.evaluators:
            result = evaluator(
                question=query,
                context=context,
                answer=response,
            )
            output.update(result)
        return output

def evaluate_article(data, trace_context):
    print("starting offline evals")

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("run_evaluators", context=trace_context) as span:
        span.set_attribute("inputs", json.dumps(data))
        configuration = AzureOpenAIModelConfiguration(
            azure_deployment="gpt-4-eval",
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        evaluator = ArticleEvaluator(configuration)
        results = evaluator(query=data['query'], context=data['context'], response=data['response'])
        resultsJson = json.dumps(results)
        span.set_attribute("output", resultsJson)

        print("results: ", resultsJson)

def evaluate_article_in_background(request, instructions, research, products, article):
    eval_data = {
        "query": json.dumps({
            "request": request,
            "instructions": instructions,
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
    thread = Thread(target=evaluate_article, args=(eval_data, trace_context,))
    thread.start()