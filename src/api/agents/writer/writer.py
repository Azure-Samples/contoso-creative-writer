import os
import json
from pathlib import Path
import prompty
from prompty.tracer import trace



@trace
def write(researchContext, research, productContext, products, assignment, feedback="No Feedback"):
    # TODO: Update this once we have the logic to parse http error codes
    try:
        result = prompty.execute(
            "writer.prompty",
            parameters={"stream": True},
            inputs={
                "researchContext": researchContext,
                "research": research,
                "productContext": productContext,
                "products": products,
                "assignment": assignment,
                "feedback": feedback,
            },
        )
    except Exception as e:
        result = {
            f"An exception occured: {str(e)}"
        }
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


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    
    base = Path(__file__).parent

    researchContext = (
        "Can you find the latest camping trends and what folks are doing in the winter?"
    )
    research = json.loads(Path(base / "research.json").read_text())
    productContext = "Can you use a selection of tents and backpacks as context?"
    products = json.loads(Path(base / "products.json").read_text())
    assignment = "Write a fun and engaging article that includes the research and product information. The article should be between 800 and 1000 words."
    result = write(researchContext, research, productContext, products, assignment)
    print(result)
