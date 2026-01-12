# check_data.py
"""Checks training and evaluation haiku data pre-SFT. 
The checks on each haiku are: 
1) it has 3 lines, 
2) the physics keyword appears verbatim (case-insensitive) once,
3) it obeys the 5-7-5 syllable count.
"""


import json
from haiku_check_helpers import check_haiku


def _check_haikus_in_jsonl(filename, verbose=False):
    """Checks all haikus in a given JSONL file.
    Prints summary of how many haikus passed/failed and details of failures.
    Returns (True, total_haikus, None) if all haikus pass. If any haiku fails, 
    returns (False, failed_haikus, failed_details).
    """
    total_haikus = 0
    failed_haikus = 0
    failed_details = []

    with open(filename, 'r') as f:
        for line in f:
            total_haikus += 1
            data = json.loads(line)
            keyword = data['keyword']
            haiku = data['haiku']

            passed, error_message = check_haiku(keyword, haiku)
            if not passed:
                failed_haikus += 1
                failed_details.append((total_haikus, f"Haiku #{total_haikus} failed: "+error_message))

    if verbose:
        print(f"--- Haiku Check Summary for {filename} ---")
        print(f"Total haikus checked: {total_haikus}")
        print(f"Total haikus failed: {failed_haikus}")

    if failed_haikus > 0:
        return False, failed_haikus, failed_details
    else:
        return True, total_haikus, None


def check_all_haikus(verbose=False):
    """Checks all haikus in all JSONL files in data/train/
    (assumes it's called from root). Checks all haikus in
    data/eval/cosmology.jsonl. Prints summary of results.
    """
    print("=== Starting training data checks ===")
    
    all_haiku_fails = []
    num_haiku_fails = 0
    
    from train_data_keywords import train_families

    for fam in train_families:
        dirname = 'data/train/'
        filename = dirname + f"{fam}.jsonl"
        print(f"\n--- Checking haikus in {filename} ---")
        all_passed, failed_haikus, failed_details = _check_haikus_in_jsonl(filename, verbose)
        if not all_passed:
            all_haiku_fails.append((filename, failed_details))
            num_haiku_fails += failed_haikus   
    
    print(f"\nFinished training data checks. Total haikus failed: {num_haiku_fails}.") 
    print("=== Starting evaluation data checks ===")

    num_haiku_fails = 0 # re-zero to now count evaluation haiku fails
    filename = 'data/eval/cosmology.jsonl'
    print(f"\n--- Checking haikus in {filename} ---")
    all_passed, failed_haikus, failed_details = _check_haikus_in_jsonl(filename, verbose)
    if not all_passed:
        all_haiku_fails.append((filename, failed_details))
        num_haiku_fails += failed_haikus  

    print(f"\nFinished evaluation data checks. Total haikus failed: {num_haiku_fails}.")

    if verbose and len(all_haiku_fails) > 0:
        for (filename, failed_details) in all_haiku_fails:
            print(f"\nFailures in file: {filename}")
            for (haiku_num, error_message) in failed_details:
                print(f"\n{error_message}")


if __name__ == "__main__":
    check_all_haikus(verbose = False)