import json
import logging
from promptflow.tracing import trace
from api.agents.researcher import researcher
from api.agents.writer import writer
from api.agents.editor import editor
from api.agents.designer import designer
from api.agents.product import product
from api.logging import log_output
from api.evaluate.evaluators import evaluate_article_in_background

from dotenv import load_dotenv
load_dotenv()

@trace
def get_research(request, instructions, feedback):
    research_result = researcher.research(
        request=request,
        instructions=instructions,
        feedback=feedback
    )

    print(json.dumps(research_result, indent=2))

    return research_result


@trace
def get_writer(request, feedback, instructions, research=[], products=[]):
    writer_reponse = writer.write(
        request=request, feedback=feedback, instructions=instructions, research=research, products=products
    )
    print(json.dumps(writer_reponse, indent=2))
    return writer_reponse


@trace
def get_editor(article, feedback):
    editor_task = editor.edit(article, feedback)

    print(json.dumps(editor_task, indent=2))
    return editor_task


@trace
def get_designer(request, instructions, feedback):
    designer_task = designer.design(request, instructions, feedback)
    print(json.dumps(designer_task, indent=2))
    return designer_task


# TODO: delete, I dont think this is used...
@trace
def regenerate_process(editor_response, context, instructions, product_documenation):
    # Get feedback for research from writer
    researchFeedback = (
        editor_response["researchFeedback"]
        if "researchFeedback" in editor_response
        else "No Feedback"
    )

    # Get feedback from writer from editor
    editorFeedback = (
        editor_response["editorFeedback"]
        if "editorFeedback" in editor_response
        else "No Feedback"
    )
    # Regenerate with feedback loop
    research_result = get_research(context, instructions, researchFeedback)
    writer_reponse = get_writer(
        context, editorFeedback, instructions, research=research_result, products=product_documenation
    )
    editor_response = get_editor(
        writer_reponse["context"]["article"], writer_reponse["context"]["feedback"]
    )
    return editor_response

@trace
def write_article(request, instructions, evaluate=False):
    log_output("Article generation started for request: %s, instructions: %s", request, instructions)

    feedback = "No Feedback"

    # Researcher task look up the info
    yield ("message", "Starting research agent task...")
    log_output("Getting researcher task output...")
    research_result = get_research(request, instructions, feedback)
    yield ("researcher", research_result)

    # Retrieve product information relevant to the user's query
    log_output("Product information...")
    product_documenation = product.get_products(request)
    yield ("products", product_documenation)

    # Then send it to the writer, the writer writes the article
    yield ("message", "Starting writer agent task...")
    log_output("Getting writer task output...")
    writer_response = get_writer(request, feedback, instructions, research=research_result, products=product_documenation)
    yield ("writer", writer_response)

    # Then send it to the editor, to decide if it's good or not
    yield ("message", "Starting editor agent task...")
    log_output("Getting editor task output...")
    editor_response = get_editor(writer_response["article"], writer_response["feedback"])
    log_output("Editor response: %s", editor_response)

    yield ("editor", editor_response)
    retry_count = 0
    while(str(editor_response["decision"]).lower().startswith("accept")):
        yield ("message", f"Sending editor feedback ({retry_count + 1})...")
        log_output("Regeneration attempt %d based on editor feedback", retry_count + 1)

        # Regenerate with feedback loop
        researchFeedback = editor_response.get("researchFeedback", "No Feedback")
        editorFeedback = editor_response.get("editorFeedback", "No Feedback")
        
        research_result = get_research(request, instructions, researchFeedback)
        yield ("researcher", research_result)

        writer_response = get_writer(request, editorFeedback, instructions, research=research_result, products=product_documenation)
        yield ("writer", writer_response)

        editor_response = get_editor(writer_response["article"], writer_response["feedback"])
        yield ("editor", editor_response)

        retry_count += 1
        if retry_count >= 2:
            break

    log_output("Editor accepted article after %d iterations", retry_count)
    yield ("message", "Editor accepted article")

    if evaluate:
        evaluate_article_in_background(
            request=request,
            instructions=instructions,
            research=research_result,
            products=product_documenation,
            article=writer_response
        )

    # Log final editor response
    log_output("Final editor response: %s", json.dumps(editor_response, indent=2))

if __name__ == "__main__":
    from api.logging import init_logging

    init_logging()
    context = "Can you find the latest camping trends and what folks are doing in the winter?"
    instructions = "Can you find the relevant information needed and good places to visit"
    for result in write_article(context, instructions, evaluate=True):
        print(*result)
