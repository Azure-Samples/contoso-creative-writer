import json
import prompty
from .researcher import researcher
from .writer import writer
from .editor import editor
from .designer import designer


@prompty.trace
def get_research(context, instructions, feedback):

    research_task = researcher.research(
        context=context,
        instructions=instructions,
        feedback=feedback,
        tools=[],
    )

    research_result = researcher.process(research_task)
    print(json.dumps(research_result, indent=2))

    return research_result


@prompty.trace
def get_writer(context, feedback, instructions, research=[]):

    writer_task = writer.write(
        context=context, feedback=feedback, instructions=instructions, research=research
    )
    writer_reponse = writer.process(writer_task)

    print(json.dumps(writer_reponse, indent=2))
    return writer_reponse


@prompty.trace
def get_editor(article, feedback):
    editor_task = editor.edit(article, feedback)

    print(json.dumps(editor_task, indent=2))
    return editor_task


@prompty.trace
def get_designer(context, instructions, feedback):
    designer_task = designer.design(context, instructions, feedback)
    print(json.dumps(designer_task, indent=2))
    return designer_task


@prompty.trace
def regenerate_process(editor_response, context, instructions):
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
        context, editorFeedback, instructions, research=research_result
    )
    editor_response = get_editor(
        writer_reponse["context"]["article"], writer_reponse["context"]["feedback"]
    )
    return editor_response


@prompty.trace
def get_article(context, instructions):
    # This code is dup in api response to ueild steped results. TODO: Fix this so its not dup later

    feedback = "No Feedback"

    # researcher task look up the info
    print("Getting researcher task output...")
    research_result = get_research(context, instructions, feedback)

    # then send it to the writer, the writer writes the article
    print("Getting writer task output...")
    writer_reponse = get_writer(
        context, feedback, instructions, research=research_result
    )

    # then send it to the editor, to decide if it's good or not
    print("Getting editor task output...")
    editor_response = get_editor(
        writer_reponse["context"]["article"], writer_reponse["context"]["feedback"]
    )
    print(editor_response)

    # retry until decision is accept or until 2x tries
    if editor_response["decision"] == "reject":
        print("Editor rejected writer, sending back to writer (1)...")
        # retry research, writer, and editor with feedback from writer and editor
        editor_response = regenerate_process(editor_response, context, instructions)

        if editor_response["decision"] == "reject":
            print("Editor rejected writer again, sending back to writer (2)...")
            # retry research, writer, and editor with feedback from writer and editor
            editor_response = regenerate_process(editor_response, context, instructions)

    print("Editor accepted writer and research, sending to designer...")
    # SETH TODO: send to designer
    # designer_task = designer.design(context, instructions, feedback)
    # create result object with editor response and writer response
    result = {"editor_response": editor_response, "writer_response": writer_reponse}
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    context = "I am writing a thought piece on early career development with Satya Nadella as an example."
    instructions = "Can you find the relevant information on both him as a person and what he studied and maybe some news articles?"
    get_article(context, instructions)
