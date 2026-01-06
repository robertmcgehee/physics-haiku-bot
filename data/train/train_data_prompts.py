# train_data_prompts.py
"""Generates training data haiku prompts for GPT-5.2 consistently."""

from train_data_keywords import train_keyword_families

prompt_num = 5  # Change from 1 to 5 to get the different prompt variations

# the 5 prompts to Cartesian product with training keywords (only for data generation, not for SFT itself)
haiku_prompts = [
'write a haiku about <keyword>',
'generate a physics haiku on <keyword>', 
'compose a haiku related to <keyword>', 
'create a haiku that describes <keyword> in physics', 
'produce a short haiku about the physics of <keyword>'
]

prompt_p0 = "Write .jsonl output where each of 25 JSON objects " \
"has three key-value pairs. The first key is 'prompt_num', the second key is " \
"'keyword' and the third key is 'haiku'. For the prompt_num value, insert" 
prompt_p1 = "For the keyword value, insert <keyword> where <keyword> is replaced " \
"by one of 25 keywords from the list"
prompt_p2 = "For the 'haiku' value," 
prompt_p3 = "where <keyword> is the same as the keyword value. " \
"Be sure to enforce a 5-7-5 syllable count, to enforce 3 line haikus, and to " \
"use the physics keyword somewhere once while sticking to the physics topic as " \
"best as you can. Make sure the first line has five syllables. Make sure the second " \
"line has seven syllables. Make sure the third line has five syllables. Use a careful " \
"algorithm to count and enforce each of the lines' syllables. If a line does not " \
"have the correct syllable count, regenerate that line until it does. " \
"Do not repeat any lines between different haikus."

if __name__ == "__main__":
    for keyword_family in train_keyword_families:
        print(f"{prompt_p0} {prompt_num}. {prompt_p1} {keyword_family}. {prompt_p2} {haiku_prompts[prompt_num - 1]} {prompt_p3}" )
        print("\n")