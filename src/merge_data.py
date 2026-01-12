# merge_data.py
"""Uses helper functions from haiku_check_helpers.py to
check all training/evaluation data haikus pre-SFT and save all good
haikus to a single, merged .jsonl file in each data/ subdirectory.
The checks on each haiku are: 
1) it has 3 lines, 
2) the physics keyword appears verbatim (case-insensitive) once,
3) it obeys the 5-7-5 syllable count.
"""


import os, json
from haiku_check_helpers import check_haiku


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

                passed, _ = check_haiku(keyword, haiku)
                if passed:
                    good_haikus += 1
                    outf.write(json.dumps(data) + "\n")
                else:
                    failed_haikus += 1

    return good_haikus, failed_haikus


def merge_all_haikus():
    """Gets good haikus from all JSONL files in data/train/ and data/eval/.
    Saves them to merged.jsonl in each data subdirectory.
    Assumes it's called from root."""

    # First, we merge the training data
    failed_haikus = 0
    good_haikus = 0
    file_out = 'data/train/merged.jsonl'
    print("=== Starting training data merge ===")
    open(file_out, "w").close() # Clear the output file first
    # find all raw .jsonl files 
    ignore_files = ['merged.jsonl', 'train_data.jsonl']
    jsonl_files = [f for f in os.listdir('data/train/') if f.endswith('.jsonl') and f not in ignore_files]
    for filename in jsonl_files:
        dirname = 'data/train/'
        filename = dirname + filename
        print(f"\n--- Getting haikus from {filename} ---")
        good_ones, bad_ones = _get_good_haikus_from_jsonl(filename, file_out)
        good_haikus += good_ones
        failed_haikus += bad_ones
    
    print(f"\nFinished training data merge.\n{good_haikus} good haikus found and saved to {file_out}.")
    print(f"{failed_haikus} bad haikus omitted.") 


    # Next, we merge the evaluation data
    file_out = 'data/eval/merged.jsonl'
    print("=== Starting evaluation data merge ===")
    open(file_out, "w").close() # Clear the output file first
    filename = 'data/eval/cosmology.jsonl'
    print(f"\n--- Getting haikus from {filename} ---")
    good_haikus, failed_haikus = _get_good_haikus_from_jsonl(filename, file_out)

    print(f"\nFinished evaluation data merge.\n{good_haikus} good haikus found and saved to {file_out}.")
    print(f"{failed_haikus} bad haikus omitted.") 


if __name__ == "__main__":
    merge_all_haikus()