from typing import List, Literal, Union
from prompty.tracer import trace
from pydantic import BaseModel, Field
import logging
import json

# agents
from agents.researcher import researcher
from agents.product import product
from agents.writer import writer
from evaluate.evaluators import evaluate_article_in_background

types = Literal["message", "researcher", "marketing", "writer", "error", "partial"]

class Message(BaseModel):
    type: types
    message: str
    data: List | dict = Field(default={})

    def to_json_line(self):
        return self.model_dump_json().replace("\n", "") + "\n"


class Task(BaseModel):
    research: str
    products: str
    assignment: str


def start_message(type: types):
    return Message(
        type="message", message=f"Starting {type} agent task..."
    ).to_json_line()


def complete_message(type: types, result: Union[dict, list] = {}):
    return Message(
        type=type, message=f"Completed {type} task", data=result
    ).to_json_line()


def error_message(error: Exception):
    return Message(
        type="error", message="An error occurred.", data={"error": str(error)}
    ).to_json_line()

def send_research(research_result):
    return json.dumps(("researcher", research_result))

def send_products(product_result):
    return json.dumps(("products", product_result))

def send_writer(full_result):
    return json.dumps(("writer", full_result))

@trace
def create(research_context, product_context, assignment_context, evaluate=False):
    #try:
    yield start_message("researcher")
    research_result = researcher.research(research_context)
    yield complete_message("researcher", research_result)

    yield start_message("marketing")
    product_result = product.find_products(product_context)
    yield complete_message("marketing", product_result)

    yield start_message("writer")
    yield complete_message("writer", {"start": True})
    writer_result = writer.write(
        research_context,
        research_result,
        product_context,
        product_result,
        assignment_context,
    )

    full_result = " "
    for item in writer_result:
        full_result = full_result + f'{item}'
        yield complete_message("partial", {"text": item})
    yield complete_message("writer", {"complete": True})

    yield send_research(research_result)
    yield send_products(product_result)
    yield send_writer(full_result)

    if evaluate:
        evaluate_article_in_background(
            research_context=research_context,
            product_context=product_context,
            assignment_context=assignment_context,
            research=research_result,
            products=product_result,
            article=full_result,
        )

@trace  
def test_create_article():
    research_context = "Can you find the latest camping trends and what folks are doing in the winter?"
    product_context = "Can you use a selection of tents and sleeping bags as context?"
    assignment_context = '''Write a fun and engaging article that includes the research and product information. 
    The article should be between 800 and 1000 words.
    Make sure to cite sources in the article as you mention the research not at the end.'''

    
    # TODO: implement logging instead of print
    for result in create(research_context, product_context, assignment_context, evaluate=True):
        parsed_result = json.loads(result)
        if type(parsed_result) is dict:
            if parsed_result['type'] == 'researcher':
                print(f"Research: ")
                print(parsed_result['data'])
                print(" ")
            if parsed_result['type'] == 'marketing':
                print("Products: ")
                print(parsed_result['data'])
                print(" ")
                print("Creating the article... ")
        if type(parsed_result) is list:
            if parsed_result[0] == "writer":
                article = parsed_result[1]
                print(f'Final Article: {article}')
                print(" ")
                print("Evaluating Results... ")
    
if __name__ == "__main__":
    from tracing import init_tracing

    tracer = init_tracing(local_tracing=True)
    test_create_article()
