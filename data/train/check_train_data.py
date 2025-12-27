# check_train_data.py
"""Checks all training data haikus pre-SFT. 
The checks on each haiku are: 
1) it has 3 lines, 
2) the physics keyword appears verbatim (case-insensitive) once or twice,
3) it obeys the 5-7-5 syllable count.
Addionally, each .jsonl file is confirmed to contain 25 haikus.
"""


import json
import re
import pronouncing, syllables
from train_data_prompts import haiku_prompts
from train_data_keywords import train_families


def _check_lines(response):
    """Checks that there are 3 lines in the response.
    If check passes, returns (True, None). If not, it returns (False, num_lines) with 
    the number of lines appearing in response."""
    lines = response.strip().split("\n")
    num_lines = len(lines)
    if num_lines == 3:
        return True, None
    else:
        return False, num_lines


chars_before_keyword = []
for prompt in haiku_prompts:
    # Get the 10 unique characters before <keyword> from each prompt template
    prompt_10chars_prior = re.search(r".{10}<keyword>", prompt).group()
    # Remove <keyword>
    prompt_10chars_prior_no_kw = re.sub(r"<keyword>", "", prompt_10chars_prior)
    chars_before_keyword.append(prompt_10chars_prior_no_kw)


def _get_keyword(prompt, prompt_num):
    """Get <keyword> from prompt based on prompt number."""
    match_str = chars_before_keyword[prompt_num - 1]
    keyword = re.search(match_str+r"(.+?)\.", prompt)
    if prompt_num == 4:
        # This prompt doesn't end with <keyword>, so we have to strip 'in physics'
        keyword = re.search(r"(.+?) in physics", keyword.group(1).strip())
    if not keyword:
        raise ValueError(f"Could not extract keyword from prompt: {prompt}")
    return keyword.group(1).strip()


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


def _check_keyword(prompt, prompt_num, response):
    """Checks that keyword appears verbatim (case-insensitive) once or twice in response.
    If check passes, returns (True, None). If not, it returns (False, num_times) with 
    the number of times keyword appears."""

    keyword = _get_keyword(prompt, prompt_num)
    keyword = _normalize_for_keyword_count(keyword)
    response = _normalize_for_keyword_count(response)
    num_times = response.count(keyword)
    if (num_times > 0) and (num_times <= 2):
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

def _check_syllables(response):
    """Checks that the haiku obeys 5-7-5 syllable count.
    If check passes, returns (True, None). If not, it returns (False, [num_syl_l1, num_syl_l2, ...])
    with syllable counts for each available line.
    Note that this will fail in addition to _check_lines if there are not exactly 3 lines."""
    
    lines = response.strip().split("\n")
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


def _check_haiku(prompt, prompt_num, response):
    """Performs all 3 checks on a single haiku and compiles useful error message if checks fail.
    Returns (True, None) if all checks pass. If any check fails, returns (False, error_message)."""
    failed_checks = []
    if _check_lines(response)[0] == False:
        failed_checks.append(f"LINE COUNT ERROR: Haiku has {_check_lines(response)[1]} lines.")
    if _check_keyword(prompt, prompt_num, response)[0] == False:
        failed_checks.append(f"KEYWORD ERROR: Keyword appears {_check_keyword(prompt, prompt_num, response)[1]} times.")
    if _check_syllables(response)[0] == False:
      failed_checks.append(f"SYLLABLE COUNT ERROR: Syllable counts per line: {_check_syllables(response)[1]}.")
    if len(failed_checks) == 0:
        return True, None
    else:
        error_message = " | ".join(failed_checks)
        return False, error_message
    

def _check_haikus_in_jsonl(filename, prompt_num, verbose=False):
    """Checks all haikus in a given JSONL file, as well as the presence of 25 haikus.
    Prints summary of how many haikus passed/failed and details of failures.
    Returns (True, total_haikus, None) if all haikus pass. If any haiku fails, or if there aren't
    25 haikus, returns (False, failed_haikus, failed_details).
    """
    total_haikus = 0
    failed_haikus = 0
    failed_details = []

    with open(filename, 'r') as f:
        for line in f:
            total_haikus += 1
            data = json.loads(line)
            prompt = data['prompt']
            response = data['response']

            passed, error_message = _check_haiku(prompt, prompt_num, response)
            if not passed:
                failed_haikus += 1
                failed_details.append((total_haikus, f"Haiku #{total_haikus} failed: "+error_message))

    if verbose:
        print(f"--- Haiku Check Summary for {filename} ---")
        print(f"Total haikus checked: {total_haikus}")
        print(f"Total haikus failed: {failed_haikus}")

    if total_haikus != 25:
        if verbose:
            print(f"HAIKU COUNT ERROR: Found {total_haikus}.")
        failed_details.append((total_haikus+1,f"HAIKU COUNT ERROR: Found {total_haikus}."))
        return False, failed_haikus, failed_details
    elif failed_haikus > 0:
        return False, failed_haikus, failed_details
    else:
        return True, total_haikus, None


def check_all_haikus(verbose=False):
    """Checks all haikus in all JSONL files under all data/train/prompt folders.
    Prints summary of results.
    """
    print("=== Starting Haiku Data Checks ===")
    
    all_haiku_fails = []
    num_haiku_fails = 0
    for prompt_num in range(1, 6):
        dirname = f"prompt{prompt_num}/"
        print(f"\n--- Checking haikus in {dirname} ---")
        for fam in train_families:
            filename = dirname+f"{fam}.jsonl"
            all_passed, failed_haikus, failed_details = _check_haikus_in_jsonl(filename, prompt_num, verbose)
            if not all_passed:
                all_haiku_fails.append((filename, failed_details))
                num_haiku_fails += failed_haikus   
    
    print(f"\nFinished Haiku Data Checks. Total files with failures: {len(all_haiku_fails)}. Total haikus failed: {num_haiku_fails}.") 
    if verbose and len(all_haiku_fails) > 0:
        for (filename, failed_details) in all_haiku_fails:
            print(f"\nFailures in file: {filename}")
            for (haiku_num, error_message) in failed_details:
                print(f"\n{error_message}")


if __name__ == "__main__":
    check_all_haikus(verbose=False)