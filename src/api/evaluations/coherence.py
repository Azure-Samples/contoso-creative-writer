import json
import prompty
import sys
from pathlib import Path

# run a batch coherence evaluation
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


# run a single coherence evaluation
@prompty.trace
def evaluate(question, context, answer):
    return prompty.execute("coherence.prompty", inputs={
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
