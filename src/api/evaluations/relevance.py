import json
import prompty
import sys
from pathlib import Path

# run a batch relevance evaluation
@prompty.trace
def batch(file):
    with open(file) as f:
        data = f.readlines()

    results = []
    for lines in data:
        data = json.loads(lines)
        result = evaluate(data["question"], data["context"], data["answer"])
        results.append(result)

    return results


# run a single relevance evaluation
@prompty.trace
def evaluate(question, context, answer):
    return prompty.execute("relevance.prompty", inputs={
        "question": question,
        "context": context,
        "answer": answer
    })


if __name__ == "__main__":
    question = sys.argv[1]
    with open(sys.argv[2]) as f:
        context = f.read()
    with open(sys.argv[3]) as f:
        answer = f.read()

    eval = evaluate(question, context, answer)
    print(eval)

    #data = Path.joinpath(Path(__file__).parent, "data.jsonl")
    #batch_eval = batch(data)
    #print(batch_eval)