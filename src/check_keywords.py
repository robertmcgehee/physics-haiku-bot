# check_keywords.py
"""Checks that all physics keywords (training, evaluation, and test)
are less than or equal to 7 syllables since we require the keyword to fit on 
a single line of the haiku.
"""


from haiku_check_helpers import _count_syllables


from train_data_keywords import train_keyword_families
for family_keywords in train_keyword_families:
    for keyword in family_keywords:
        num_syllables = 0
        # some keywords are multiple words, so count syllables for each word and add them
        # since we want the entire keyword phrase to fit on a single line of the haiku
        for word in keyword.split():
            num_syllables += _count_syllables(word)
        if num_syllables > 7:
            print(f"Keyword '{keyword}' fails since it has {num_syllables} syllables.")

from eval_data_keywords import cosmology_keywords
for keyword in cosmology_keywords:
    num_syllables = 0
    # some keywords are multiple words, so count syllables for each word and add them
    # since we want the entire keyword phrase to fit on a single line of the haiku
    for word in keyword.split():
        num_syllables += _count_syllables(word)
    if num_syllables > 7:
        print(f"Keyword '{keyword}' fails since it has {num_syllables} syllables.")

from test_data_keywords import particle_physics_keywords
for keyword in particle_physics_keywords:
    num_syllables = 0
    # some keywords are multiple words, so count syllables for each word and add them
    # since we want the entire keyword phrase to fit on a single line of the haiku
    for word in keyword.split():
        num_syllables += _count_syllables(word)
    if num_syllables > 7:
        print(f"Keyword '{keyword}' fails since it has {num_syllables} syllables.")