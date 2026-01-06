# check_train_data.py
"""Checks all training data haikus pre-SFT. 
The checks on each haiku are: 
1) it has 3 lines, 
2) the physics keyword appears verbatim (case-insensitive) once,
3) it obeys the 5-7-5 syllable count.
"""


import json
import re
import pronouncing, syllables
from train_data_keywords import train_families


def _check_lines(haiku):
    """Checks that there are 3 lines in the haiku.
    If check passes, returns (True, None). If not, it returns (False, num_lines) with 
    the number of lines appearing in haiku."""
    lines = haiku.strip().split("\n")
    num_lines = len(lines)
    if num_lines == 3:
        return True, None
    else:
        return False, num_lines


def _normalize_for_keyword_count(text):
    """Normalizes text for keyword counting by converting to lowercase, converting
    all dashes/hyphens to spaces, and collapasing whitespaces. Important to prevent
    false errors for keywords like 'non-inertial' or 'four-vector'."""
    # while some physics keywords like 'Hamiltonian' should be capitalized, I won't enforce that
    text = text.lower()
    # normalize hyphen/dash variants to spaces
    text = re.sub(r"[-–—−]", " ", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _check_keyword(keyword, haiku):
    """Checks that keyword appears verbatim (case-insensitive) once in haiku.
    If check passes, returns (True, None). If not, it returns (False, num_times) with 
    the number of times keyword appears."""

    keyword = _normalize_for_keyword_count(keyword)
    haiku = _normalize_for_keyword_count(haiku)
    num_times = haiku.count(keyword)
    if num_times == 1:
        return True, None
    else:
        return False, num_times
    

def _count_syllables(word):
    """Counts syllables in word. Tries to use pronouncing library first which is based
    on CMUdict, but falls back on syllables if word not available in pronouncing."""
    word = re.sub(r"[^a-zA-Z']", "", word.lower())
    phones = pronouncing.phones_for_word(word)
    # if word not found in pronouncing, fall back on pyphen hyphenation estimate
    if not phones:
        return syllables.estimate(word)
    return pronouncing.syllable_count(phones[0])

def _check_syllables(haiku):
    """Checks that the haiku obeys 5-7-5 syllable count.
    If check passes, returns (True, None). If not, it returns (False, [num_syl_l1, num_syl_l2, ...])
    with syllable counts for each available line.
    Note that this will fail in addition to _check_lines if there are not exactly 3 lines."""
    
    lines = haiku.strip().split("\n")
    expected_count = [5, 7, 5] # standard haiku syllable counts
    actual_count = []
    passed = True
    for i, line in enumerate(lines):
        words = line.split()
        syllables = 0
        for word in words:
            syllables += _count_syllables(word)
        # If there are more than 3 lines, continue printing syllable counts for all lines
        actual_count.append(syllables)
        if i >= len(expected_count):
            passed = False
        elif syllables != expected_count[i]:
            passed = False 
    
    # Want to flag the syllable count if there are less than 3 lines as well
    if i < 2:
        passed = False

    if passed:
        return passed, None
    else:
        return passed, actual_count


def _check_haiku(keyword, haiku):
    """Performs all 3 checks on a single haiku and compiles useful error message if checks fail.
    Returns (True, None) if all checks pass. If any check fails, returns (False, error_message)."""
    failed_checks = []
    if _check_lines(haiku)[0] == False:
        failed_checks.append(f"LINE COUNT ERROR: Haiku has {_check_lines(haiku)[1]} lines.")
    if _check_keyword(keyword, haiku)[0] == False:
        failed_checks.append(f"KEYWORD ERROR: Keyword appears {_check_keyword(keyword, haiku)[1]} times.")
    if _check_syllables(haiku)[0] == False:
      failed_checks.append(f"SYLLABLE COUNT ERROR: Syllable counts per line: {_check_syllables(haiku)[1]}.")
    if len(failed_checks) == 0:
        return True, None
    else:
        error_message = " | ".join(failed_checks)
        return False, error_message
    

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

            passed, error_message = _check_haiku(keyword, haiku)
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
    Prints summary of results.
    """
    print("=== Starting Haiku Data Checks ===")
    
    all_haiku_fails = []
    num_haiku_fails = 0
    
    for fam in train_families:
        filename = f"{fam}.jsonl"
        print(f"\n--- Checking haikus in {filename} ---")
        all_passed, failed_haikus, failed_details = _check_haikus_in_jsonl(filename, verbose)
        if not all_passed:
            all_haiku_fails.append((filename, failed_details))
            num_haiku_fails += failed_haikus   
    
    print(f"\nFinished Haiku Data Checks. Total haikus failed: {num_haiku_fails}.") 
    if verbose and len(all_haiku_fails) > 0:
        for (filename, failed_details) in all_haiku_fails:
            print(f"\nFailures in file: {filename}")
            for (haiku_num, error_message) in failed_details:
                print(f"\n{error_message}")


if __name__ == "__main__":
    check_all_haikus(verbose=False)