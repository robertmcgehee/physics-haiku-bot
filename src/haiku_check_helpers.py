# haiku_check_helpers.py
"""Helper functions used to check haikus for consistency with
3 lines, keyword inclusion, and syllable counts.
"""


import re
import pronouncing, syllables


def check_lines(haiku):
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


def check_keyword(keyword, haiku):
    """Checks that keyword appears verbatim (case-insensitive) once in haiku.
    If check passes, returns (True, num_times). If not, it returns (False, num_times) with 
    the number of times keyword appears."""

    keyword = _normalize_for_keyword_count(keyword)
    haiku = _normalize_for_keyword_count(haiku)
    num_times = haiku.count(keyword)
    if num_times == 1:
        return True, num_times
    else:
        return False, num_times
    

def _count_syllables(word):
    """Counts syllables in word. Tries to use pronouncing library first which is based
    on CMUdict, but falls back on syllables if word not available in pronouncing."""

    # we need to be careful about hyphens since some physics keywords contain them
    # split on hyphen/dash variants first (so non-inertial -> ["non", "inertial"])
    parts = re.split(r"[-–—−]+", word)

    total = 0
    for part in parts:
        part = re.sub(r"[^a-zA-Z']", "", part.lower())
        if not part:
            continue
        phones = pronouncing.phones_for_word(part)
        # if word not found in pronouncing, fall back on pyphen hyphenation estimate
        if not phones:
            total += syllables.estimate(part)
        else:
            total += pronouncing.syllable_count(phones[0])
    return total


def check_syllables(haiku, givelinetruth = False):
    """Checks that the haiku obeys 5-7-5 syllable count.
    Returns (passed_status, [num_syl_l1, ..., ...]) with syllable counts for each available line.
    Note that this only checks the first 3 lines. It does not fail if there are more
    (or fewer than) 3 lines, only if the lines don't match their required syllable count.
    If givelinetruth == True, then also pass a boolean list for the lines passing/failing."""
    
    
    lines = haiku.strip().split("\n")
    expected_count = [5, 7, 5] # standard haiku syllable counts
    actual_count = []
    line_truth = []

    for i, line in enumerate(lines[:3]):
        words = line.split()
        syllables = 0
        for word in words:
            syllables += _count_syllables(word)
        actual_count.append(syllables)
        if syllables != expected_count[i]:
            line_truth.append(False)
        else:
            line_truth.append(True)
    
    passed = all(line_truth) # only pass if all lines are syllable accurate

    if givelinetruth == True:
        return passed, actual_count, line_truth
    else:
        return passed, actual_count
    

def check_haiku(keyword, haiku):
    """Performs all 3 checks on a single haiku and compiles useful error message if checks fail.
    Returns (True, None) if all checks pass. If any check fails, returns (False, error_message)."""
    failed_checks = []
    if check_lines(haiku)[0] == False:
        failed_checks.append(f"LINE COUNT ERROR: Haiku has {check_lines(haiku)[1]} lines.")
    if check_keyword(keyword, haiku)[0] == False:
        failed_checks.append(f"KEYWORD ERROR: Keyword appears {check_keyword(keyword, haiku)[1]} times.")
    if check_syllables(haiku)[0] == False:
      failed_checks.append(f"SYLLABLE COUNT ERROR: Syllable counts per line: {check_syllables(haiku)[1]}.")
    if len(failed_checks) == 0:
        return True, None
    else:
        error_message = " | ".join(failed_checks)
        return False, error_message