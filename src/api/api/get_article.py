import random
from flask import Blueprint, Flask, jsonify, request, stream_with_context, Response
import json
import logging
from agents.orchestrator import (
    get_research,
    get_writer,
    get_editor,
    get_designer,
    regenerate_process,
)
from flask_cors import cross_origin

bp = Blueprint("names", __name__)

def _create_json_response(type, contents):
    return ">>>" + json.dumps({
        "type": type,
        "contents": contents
    })


# Route to call sales prompty that takes in a customer id and a question
@bp.route("/get_article")
@cross_origin()
@stream_with_context
def get_article():
    context = request.args.get("context")
    instructions = request.args.get("instructions")
    feedback = "No Feedback"

    logging.info("Article generation started for context: %s, instructions: %s", context, instructions)

    # Researcher task look up the info
    yield _create_json_response("message", "Starting research agent task...")
    logging.debug("Getting researcher task output...")
    research_result = get_research(context, instructions, feedback)
    yield _create_json_response("researcher", research_result)

    # Then send it to the writer, the writer writes the article
    yield _create_json_response("message", "Starting writer agent task...")
    logging.debug("Getting writer task output...")
    writer_response = get_writer(context, feedback, instructions, research=research_result)
    yield _create_json_response("writer", writer_response["context"])

    # Then send it to the editor, to decide if it's good or not
    yield _create_json_response("message", "Starting editor agent task...")
    logging.debug("Getting editor task output...")
    editor_response = get_editor(writer_response["context"]["article"], writer_response["context"]["feedback"])
    logging.debug("Editor response: %s", editor_response)

    yield _create_json_response("editor", editor_response)
    retry_count = 0
    while(str(editor_response["decision"]).lower().startswith("accept")):
        yield _create_json_response("message", f"Sending editor feedback ({retry_count + 1})...")
        logging.info("Regeneration attempt %d based on editor feedback", retry_count + 1)

        # Regenerate with feedback loop
        researchFeedback = editor_response.get("researchFeedback", "No Feedback")
        editorFeedback = editor_response.get("editorFeedback", "No Feedback")
        
        research_result = get_research(context, instructions, researchFeedback)
        yield _create_json_response("researcher", research_result)

        writer_response = get_writer(context, editorFeedback, instructions, research=research_result)
        yield _create_json_response("writer", writer_response["context"])

        editor_response = get_editor(writer_response["context"]["article"], writer_response["context"]["feedback"])
        yield _create_json_response("editor", editor_response)

        retry_count += 1
        if retry_count >= 2:
            break

    logging.info("Editor accepted article after %d iterations", retry_count)
    yield _create_json_response("message", "Editor accepted article")

    # Log final editor response
    logging.debug("Final editor response: %s", json.dumps(editor_response, indent=2))
    return Response(get_article(), mimetype="application/json")
