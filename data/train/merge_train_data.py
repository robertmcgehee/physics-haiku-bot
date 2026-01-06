# merge_train_data.py
"""Uses helper functions from check_train_data.py to
check all training data haikus pre-SFT and save all good
haikus to a single, merged .jsonl file.
The checks on each haiku are: 
1) it has 3 lines, 
2) the physics keyword appears verbatim (case-insensitive) once or twice,
3) it obeys the 5-7-5 syllable count.
"""


import os, json
from check_train_data import _check_haiku


def _get_good_haikus_from_jsonl(filename, file_out):
    """Gets all good haikus from a JSONL file and writes them to file_out.
    Returns a tuple of good haikus count and failed haikus count."""
    failed_haikus = 0
    good_haikus = 0
    with open(file_out, 'a', encoding='utf-8') as outf:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                keyword = data['keyword']
                haiku = data['haiku']

                passed, _ = _check_haiku(keyword, haiku)
                if passed:
                    good_haikus += 1
                    outf.write(json.dumps(data) + "\n")
                else:
                    failed_haikus += 1

    return good_haikus, failed_haikus


def merge_all_haikus(file_out = "merged_haikus.jsonl"):
    """Gets good haikus from all JSONL files (excluding file_out) in current folder.
    Saves them to file_out."""
    failed_haikus = 0
    good_haikus = 0
    print("=== Starting Haiku Data Merge ===")
    open(file_out, "w").close() # Clear the output file first
    # find all .jsonl files not including the output file
    jsonl_files = [f for f in os.listdir('.') if f.endswith('.jsonl') and f != file_out]
    for filename in jsonl_files:
        print(f"\n--- Getting haikus from {filename} ---")
        good_ones, bad_ones = _get_good_haikus_from_jsonl(filename, file_out)
        good_haikus += good_ones
        failed_haikus += bad_ones
    
    print(f"\nFinished Haiku Data Merge.\n{good_haikus} good haikus found and saved to {file_out}.")
    print(f"{failed_haikus} bad haikus omitted.") 


if __name__ == "__main__":
    merge_all_haikus()