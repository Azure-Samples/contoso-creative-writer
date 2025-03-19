import os
import json
from pathlib import Path
import prompty
from prompty.tracer import trace



@trace
def publish(article, styleGuide, feedback="No Feedback"):
    # TODO: Update this once we have the logic to parse http error codes
    try:
        result = prompty.execute(
            "publisher.prompty",
            parameters={"stream": True},
            inputs={
                "article": article,
                "styleGuide": styleGuide,
                "feedback": feedback,
            },
        )
    except Exception as e:
        result = {
            f"An exception occured: {str(e)}"
        }
    return result

def process(formatted_content):
    # parse string this character --- , formatted article and feedback
    result = formatted_content.split("---")
    formatted_article = str(result[0]).strip()
    if len(result) > 1:
        feedback = str(result[1]).strip()
    else:
        feedback = "No Feedback"

    return {
        "formatted_article": formatted_article,
        "feedback": feedback,
    }


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    
    base = Path(__file__).parent

    # First get the article from the writer
    from writer import write, process as writer_process
    
    researchContext = (
        "Can you find the latest camping trends and what folks are doing in the winter?"
    )
    research = json.loads(Path(base / "research.json").read_text())
    productContext = "Can you use a selection of tents and backpacks as context?"
    products = json.loads(Path(base / "products.json").read_text())
    assignment = "Write a fun and engaging article that includes the research and product information. The article should be between 800 and 1000 words."
    
    writer_result = write(researchContext, research, productContext, products, assignment)
    processed_writer = writer_process(writer_result)
    article = processed_writer["article"]
    
    # Now format the article using the publisher agent
    styleGuide = """
    # Contoso Style Guide
    - Use H2 for main headings and H3 for subheadings
    - All product names should be in bold
    - All links should use the format [text](url)
    - Add the Contoso logo at the top of the article
    - Include a "Share this article" section at the bottom
    - Use the Contoso color scheme: #0078D4 for headings, #333333 for body text
    """
    
    result = publish(article, styleGuide)
    formatted_content = process(result)
    print(formatted_content["formatted_article"])
