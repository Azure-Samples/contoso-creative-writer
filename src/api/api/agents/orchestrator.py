import json
from promptflow.tracing import trace, start_trace
from api.agents.researcher import researcher
from api.agents.writer import writer
from api.agents.editor import editor
from api.agents.designer import designer
from api.agents.product import product
from dotenv import load_dotenv
load_dotenv()

@trace
def get_research(context, instructions, feedback):

    research_result = researcher.research(
        context=context,
        instructions=instructions,
        feedback=feedback
    )

    print(json.dumps(research_result, indent=2))

    return research_result


@trace
def get_writer(context, feedback, instructions, research=[], products=[]):

    writer_reponse = writer.write(
        context=context, feedback=feedback, instructions=instructions, research=research, products=products
    )
    print(json.dumps(writer_reponse, indent=2))
    return writer_reponse


@trace
def get_editor(article, feedback):
    editor_task = editor.edit(article, feedback)

    print(json.dumps(editor_task, indent=2))
    return editor_task


@trace
def get_designer(context, instructions, feedback):
    designer_task = designer.design(context, instructions, feedback)
    print(json.dumps(designer_task, indent=2))
    return designer_task


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
def get_article(context, instructions):
    # This code is dup in api response to ueild steped results. TODO: Fix this so its not dup later

    feedback = ""
    print("Getting article for context: ", context)

    # researcher task look up the info
    print("Getting researcher task output...")
    research_result = get_research(context, instructions, feedback)
    product_documenation = product.get_products(context)

    # then send it to the writer, the writer writes the article
    print("Getting writer task output...")
    writer_reponse = get_writer(
        context, feedback, instructions, research=research_result, products=product_documenation
    )

    # then send it to the editor, to decide if it's good or not
    print("Getting editor task output...")
    editor_response = get_editor(
        writer_reponse["article"], writer_reponse["feedback"]
    )
    print(editor_response)

    # retry until decision is accept or until 2x tries
    if editor_response["decision"] == "reject":
        print("Editor rejected writer, sending back to writer (1)...")
        # retry research, writer, and editor with feedback from writer and editor
        editor_response = regenerate_process(editor_response, context, instructions, product_documenation)

        if editor_response["decision"] == "reject":
            print("Editor rejected writer again, sending back to writer (2)...")
            # retry research, writer, and editor with feedback from writer and editor
            editor_response = regenerate_process(editor_response, context, product_documenation)

    print("Editor accepted writer and research, sending to designer...")
    # SETH TODO: send to designer
    # designer_task = designer.design(context, instructions, feedback)
    # create result object with editor response and writer response
    result = {"editor_response": editor_response, "writer_response": writer_reponse}
    print(json.dumps(result, indent=2))
    return result
 
if __name__ == "__main__":
    import os
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
    from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
    from promptflow.tracing._integrations._openai_injector import inject_openai_api

    # log to app insights if configured
    if 'APPLICATIONINSIGHTS_CONNECTION_STRING' in os.environ:
        inject_openai_api()

        connection_string=os.environ['APPLICATIONINSIGHTS_CONNECTION_STRING']
        trace.set_tracer_provider(TracerProvider(sampler=ParentBasedTraceIdRatio(1.0)))
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(AzureMonitorTraceExporter(connection_string=connection_string)))

    if 'PROMPTFLOW_TRACING_SERVER' in os.environ and os.environ['PROMPTFLOW_TRACING_SERVER'] != 'false':
        start_trace()

    context = "Can you find the latest camping trends and what folks are doing in the winter?"
    instructions = "Can you find the relevant information needed and good places to visit"
    get_article(context, instructions)
