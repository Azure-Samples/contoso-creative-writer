import json

from flask import Blueprint, request, stream_with_context, Response
from opentelemetry import trace
from api.agents.orchestrator import write_article

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
    evaluate = False
    span = trace.get_current_span()
    if (span.is_recording):
        evaluate = True

    for result in write_article(context, instructions, evaluate):
        yield _create_json_response(*result)

    return Response(get_article(), mimetype="application/json")

