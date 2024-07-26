import os
import json
from pathlib import Path
import prompty
from prompty.tracer import trace

base = Path(__file__).parent


@trace
def write(researchContext, research, productContext, products, assignment):

    result = prompty.execute(
        "writer.prompty",
        parameters={"stream": True, "max_tokens": 2000},
        inputs={
            "researchContext": researchContext,
            "research": research,
            "productContext": productContext,
            "products": products,
            "assignment": assignment,
        },
    )
    return result


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    researchContext = (
        "Can you find the latest camping trends and what folks are doing in the winter?"
    )
    research = json.loads(Path(base / "research.json").read_text())
    productContext = "Can you use a selection of tents and backpacks as context?"
    products = json.loads(Path(base / "products.json").read_text())
    assignment = "Write a fun and engaging article that includes the research and product information. The article should be between 800 and 1000 words."
    result = write(researchContext, research, productContext, products, assignment)
    print(result)
