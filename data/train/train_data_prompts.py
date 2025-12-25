# train_data_prompts.py
# Wrapper to generate training data haiku prompts for GPT-5.2 consistently.

from train_data_keywords import train_keyword_families

# 5 prompts to Cartesian product with training keywords
haiku_prompts = [
'"Write a haiku about <keyword>."',
'"Generate a physics haiku on <keyword>."', 
'"Compose a haiku related to <keyword>."', 
'"Create a haiku that describes <keyword> in physics."', 
'"Produce a short haiku about the physics of <keyword>."'
]

prompt_begin = "Create a .jsonl file where each of 25 JSON objects " \
"has two key-value pairs. The first key is 'prompt' and the second key is " \
"'response'. For the prompt value, please insert"
prompt_middle = 'where <keyword> is replaced by one of 25 keywords from the list '
prompt_end = "For the 'response' value, please do as the 'prompt' value asks. " \
"Be sure to enforce a 5-7-5 syllable count, to enforce 3 line haikus, and to " \
"use the physics keyword somewhere once while sticking to the physics topic as " \
"best as you can."

for keyword_family in train_keyword_families:
    print(f"{prompt_begin} {haiku_prompts[4]} {prompt_middle} {keyword_family}. {prompt_end}" )
    print("\n")