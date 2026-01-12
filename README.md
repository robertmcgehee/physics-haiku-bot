# Physics Haiku Bot

## Overview

This project explores whether a small, carefully curated dataset is sufficient to fine-tune a smaller model like DistilGPT-2 to reliably generate structured creative outputs in the form of physics haikus. Even SOTA LLMs like GPT-5.2 struggle to reliably produce such haikus. I find failure rates as high as 25% even with explicit prompting during data generation. Thus, this is no easy task for a small model to tackle.

This repository contains training data (i.e. physics haikus in JSONL files), an SFT notebook, and an SFT- vs base-model scoreboard. The raw haikus are organized by physics concept family and criteria-passing haikus are merged into a single training data JSONL and a single evaluation data JSONL. The haikus were generated using ChatGPT-5.2. This repo also contains functions to check haikus for consistency, merge good haikus, format haiku data before SFT, and other helper functions used to generate data haiku prompts. 

For a snapshot of current progress, **see results/SCOREBOARD.md**.

## Research Goal

To study whether a small model can learn a rigid output format (5/7/5 syllables, 3 lines, keyword inclusion) from a carefully curated dataset while experimenting with data formatting, SFT, and RL techniques.

## Key Files

- src/*_data_keywords.py contains the training, evaluation, or test family physics keywords
- src/*_data_prompts.py outputs the prompts used to generate the training or evaluation haiku data
- src/check_data.py checks all training and evaluation data for haiku consistency; prints a high-level summary; set verbose=True for more details
- src/merge_data.py saves all criteria-passing data to data/*/merged.jsonl 
- src/format_data.py adds formatted 'prompt' and 'response' key-value pairs to haiku JSON objects before SFT  
- data/train/ contains all unfiltered, raw training haikus in concept-family JSONL files
- data/eval/cosmology.jsonl contains all unfiltered, raw evaluation haikus
- data/train/merged.jsonl and data/eval/merged.jsonl contain the good haikus for SFT BEFORE formatting 
- data/train/train_data.jsonl and data/eval/eval_data.jsonl contain the 1526 / 2000 and 157 / 250 good haikus for SFT AFTER formatting; **these are for SFT**
- notebooks/sft.ipynb loads good training/evaluation haikus and performs SFT on DistilGPT-2 
- notebooks/test_models.ipynb evaluates zero-shot base, few-shot base, and SFT models on test haiku keywords
- results/ contains results from test_models, including generated test haikus for each model and SCOREBOARD.md

## Next Steps
- (high priority) reward-based fine-tuning to improve SFT model for the hard structural haiku constraints
- (low priority) make haiku checks robust to few-shot base model 'cheating' so that its accuracy on the SCOREBOARD is meaningful
- (low priority) verify that there are no repeated phrases (>= 3 words) in the training/evaluation data; possibility minimal due to data generation practices (only 25 haikus at a time, prompt variety, by-eye inspection), but non-zero