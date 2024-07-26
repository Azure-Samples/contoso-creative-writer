from typing import List, Literal, Union
from prompty.tracer import trace
from pydantic import BaseModel, Field

# agents
from agents.researcher import researcher
from agents.product import product
from agents.writer import writer

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


@trace
def start_message(type: types):
    return Message(
        type="message", message=f"Starting {type} agent task..."
    ).to_json_line()


@trace
def complete_message(type: types, result: Union[dict, list] = {}):
    return Message(
        type=type, message=f"Completed {type} task", data=result
    ).to_json_line()


@trace
def error_message(error: Exception):
    return Message(
        type="error", message="An error occurred.", data={"error": str(error)}
    ).to_json_line()


@trace
async def create(research_context, product_context, assignment_context):
    try:
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
        for item in writer_result:
            yield complete_message("partial", {"text": item})

        yield complete_message("writer", {"complete": True})

    except Exception as e:
        yield error_message(e)
