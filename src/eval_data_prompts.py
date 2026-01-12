# eval_data_prompts.py
"""Generates evaluation data haiku prompts for GPT-5.2 consistently
using the same style and wording as train_data_prompts."""


prompt_num = 5

from train_data_prompts import haiku_prompts, prompt_p0, prompt_p1, prompt_p2, prompt_p3
from eval_data_keywords import cosmology_keywords

if __name__ == "__main__":
    print(f"{prompt_p0} {prompt_num}. {prompt_p1} {cosmology_keywords}. {prompt_p2} {haiku_prompts[prompt_num - 1]} {prompt_p3}" )
    print("\n")