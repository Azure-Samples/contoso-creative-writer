import json
import sys
import pathlib

# input_file = "eval_results.jsonl"
# output_file = "genai_evals_data.jsonl"

if len(sys.argv) != 3:
    print("Usage: python genai_evals_convert.py input_file output_file")
    sys.exit(1)
else:
    # TODO: remove this print
    print("Converting to genai-evals data format...\n", sys.argv[1], "\n", sys.argv[2])

# Get input_file from the first parameters
input_file = sys.argv[1]
output_file = sys.argv[2]

# current_folder = pathlib.Path(__file__).parent.resolve()
# with open(current_folder.joinpath(input_file), 'r') as f:
with open(input_file, 'r') as f:
    content = f.read()  # Reads the entire file into a string
eval_results = json.loads(content)

# with open(current_folder.joinpath(output_file), 'w') as f:
with open(output_file, 'w') as f:
    for row in eval_results["rows"]:
        new_row = {
            "query": row["inputs.query"],
            "context": row["inputs.context"],
            "response": row["inputs.response"],
        }
        f.write(json.dumps(new_row) + "\n")

print("Converted to genai-evals data format")
