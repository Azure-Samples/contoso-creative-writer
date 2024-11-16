import json
import sys
import uuid

if len(sys.argv) != 3:
    print("Usage: python genai_evals_convert.py input_file output_file")
    sys.exit(1)
else:
    # TODO: remove this print
    print("Converting to genai-evals data format...\n", sys.argv[1], "\n", sys.argv[2])

# Get input_file from the first parameters
input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as f:
    content = f.read()  # Reads the entire file into a string
eval_results = json.loads(content)

with open(output_file, 'w') as f:
    for index, row in enumerate(eval_results["rows"]):
        description = {
            "context": {
                "system-prompt": f"Test {index + 1}",
            },
        }

        new_row = {
            "id": uuid.uuid4().hex,
            "description": json.dumps(description),
            "query": row["inputs.query"],
            "context": row["inputs.context"],
            "response": row["inputs.response"],
            "ground_truth": "",
        }
        f.write(json.dumps(new_row) + "\n")

print("Converted to genai-evals data format")
