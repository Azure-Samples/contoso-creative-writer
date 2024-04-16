import prompty
import sys
import json


def write(context, feedback, instructions, research = []):
    result = prompty.execute(
        "writer.prompty",
        inputs={
            "context": context,
            "feedback": feedback,
            "instructions": instructions,
            "research": research,
        },
    )
    return result

def process(writer):
    # parse string this chracter --- , artcile and feedback
    result = writer.split("---")
    article = str(result[0]).strip()
    if len(result) > 1:
        feedback = str(result[1]).strip()
    else:
        feedback = "No Feedback"

    return {
        "context": {
            "article": article,
            "feedback": feedback,
        }
    }
if __name__ == "__main__":
    # get args from the user
    # check if args if null default to a value
    # if len(sys.argv) == 0:
    #     context="I want to write an article about Satya Nadella and the beginnings of his career.",
    #     feedback="No Feedback",
    #     instructions="Can you help me find information about Satya Nadella's career and beginnings?"
    #     research = []
    # else:
    context = sys.argv[1]
    feedback = sys.argv[2]
    instructions = sys.argv[3]
    research = json.dumps(sys.argv[4])
    result = write(
        context=str(context),
        feedback=str(feedback),
        instructions=str(instructions),
        research=research,
    )
    processed = process(result)
    print(processed)
