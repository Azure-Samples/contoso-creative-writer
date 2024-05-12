import sys
import json
import jsonlines
import os

from promptflow.tracing import trace as pftrace
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.core import Flow
from pathlib import Path

from api.evaluate.writer import WriterEvaluator
from threading import Thread

from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace import set_span_in_context
folder = Path(__file__).parent.absolute().as_posix()

def run_evaluators(data, trace_context):
    print("starting offline evals")

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("run_evaluators", context=trace_context) as span:
        span.set_attribute("inputs", str(data))
        configuration = AzureOpenAIModelConfiguration(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        evaluator = WriterEvaluator(configuration)
        results = evaluator(query=data['query'], context=data['context'], response=data['response'])
        span.set_attribute("outputs", str(results))

        print("results: ", results)



def trace_eval_data(data):
    span = trace.get_current_span()
    # only run evaluators if data is being recorded
    if (span.is_recording):
        # propagate trace context to new thread, TODO: not quite working
        trace_context = set_span_in_context(span)
        thread = Thread(target=run_evaluators, args=(data, trace_context,))
        thread.start()

def log_eval_data(context, feedback, instructions, research, products, result):
    # log evaluation data
    query = str({
        'article_request': context, 
        'research_instructions': instructions,
        'editor_feedback': feedback
    })
    context = str({
        'research': research,
        'products': products,
    })
    data = {'query': query, 'context': context, 'response': result}
    trace_eval_data(data)

    if os.environ.get('WRITE_EVAL_DATA'):
        with jsonlines.open('output.jsonl', 'a') as writer:
            writer.write(data)

@pftrace
def execute(context, feedback, instructions, research, products):
    # Load prompty with AzureOpenAIModelConfiguration override
    configuration = AzureOpenAIModelConfiguration(
        azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    override_model = {
        "configuration": configuration,
        "parameters": {"max_tokens": 512}
    }
        # create path to prompty file
    prompty_file = folder + "/writer.prompty"
    loaded_prompty = Flow.load(prompty_file, model=override_model)
    result = loaded_prompty(
        context=context,
        feedback=feedback,
        instructions=instructions,
        research=research,
        products=products
    )

    log_eval_data(context, feedback, instructions, research, products, result)
    return result


def process(writer):
    # parse string this chracter --- , article and feedback
    result = writer.split("---")
    article = str(result[0]).strip()
    if len(result) > 1:
        feedback = str(result[1]).strip()
    else:
        feedback = "No Feedback"

    return {
        "article": article,
        "feedback": feedback,
    }


def write(context, feedback, instructions, research, products):
    result = execute(
        context=context,
        feedback=feedback,
        instructions=instructions,
        research=research,
        products=products
    )
    processed = process(result)
    return processed


if __name__ == "__main__":
    # get args from the user
    # context = "Can you find the latest camping trends and what folks are doing in the winter?"
    # feedback = "Research Feedback:\nAdditional specifics on how each phase of his education directly influenced particular career decisions or leadership styles at Microsoft would enhance the narrative. Information on key projects or initiatives that Nadella led, correlating to his expertise gained from his various degrees, would add depth to the discussion on the interplay between his education and career milestones."
    # instructions = "Can you find the relevant information on both him as a person and what he studied and maybe some news articles?"
    # research = []
    context = sys.argv[1]
    feedback = sys.argv[2]
    instructions = sys.argv[3]
    research = json.dumps(sys.argv[4])
    result = execute(
        context=str(context),
        feedback=str(feedback),
        instructions=str(instructions),
        research=research,
    )
    processed = process(result)
    print(processed)
