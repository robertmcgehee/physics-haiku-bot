# format_data.py
"""Formats haiku data for SFT by adding 'prompt' and 'response' key-value 
pairs to JSON objects in training and evaluation data. Purpose is to allow 
quick experiments with SFT training to see how it depends on data 
formatting choices. Run from root.
"""


import json


def change_format(filename, file_out):
    open(file_out, "w").close() # Clear the output file first
    print(f"Re-formatting data from {filename} and saving to {file_out}.")
    with open(file_out, 'a', encoding='utf-8') as outf:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                keyword = data['keyword']
                haiku = data['haiku']
                lines = haiku.strip().split("\n")
                # Change 'prompt' and/or 'response' formats used in SFT training here
                data['prompt'] = "Write 3 lines about Keyword: " + keyword  + "\n1)\n2)\n3)"
                data['response'] = "1) " + lines[0] + "\n2) " + lines[1] + "\n3) " + lines[2] + "\n<END>"
                outf.write(json.dumps(data) + "\n")


if __name__ == "__main__":
    change_format('data/train/merged.jsonl', 'data/train/train_data.jsonl')
    change_format('data/eval/merged.jsonl', 'data/eval/eval_data.jsonl')