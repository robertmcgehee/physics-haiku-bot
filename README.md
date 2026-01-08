# Physics Haiku Bot

## Overview

This project explores whether a small, carefully curated dataset is sufficient to fine-tune a smaller model like DistilGPT-2 to reliably generate structured creative outputs in the form of physics haikus. Even SOTA LLMs like GPT-5.2 struggle to reliably produce such haikus with failure rates as high as 27% even with explicit prompting. Thus, this is no easy task for a small model to tackle.

This repository contains SFT training data (i.e. physics haikus in JSONL files), an SFT training notebook, and an SFT vs base-model scoreboard. The raw haikus are organized by physics concept family and criteria-passing haikus are merged into a single training data JSONL and a single evaluation data JSONL. The haikus were generated using ChatGPT-5.2. This repo also contains functions to check haikus for consistency, merge good haikus, format haiku data before SFT, and other helper functions used to generate data haiku prompts. 

For a snapshot of current progress, **see results/SCOREBOARD.md**.

## Research Goal

To study whether a small model can learn a rigid output format (5/7/5 syllables, 3 lines, keyword inclusion) from a carefully curated dataset while experimenting with data formatting, SFT, and RL techniques.

## Status 

To be implemented next: per-line syllable scoring for better evaluation metric; custom haiku-consistency checks each evaluation step *during* training to see how those metrics progress. Short term: GRPO training after SFT

## Key Files

- data/train/train_data_prompts.py contains the exact prompts used to generate the haikus
- data/train/ contains all unfiltered, raw training haikus
- data/train/check_train_data.py checks all training haikus for 1) 3 lines, 2) physics keyword use, and 3) correct syllable count; prints a high-level summary; set verbose=True for more details
- data/train/merge_train_data.py saves all criteria-passing haikus to a single, merged JSONL file
- data/train/format_haikus.py adds formatted 'prompt' and 'response' key-value pairs to haiku JSON objects before SFT training 
- data/eval/ contains all unfiltered, raw evaluation haikus
- data/train/merged_haikus.jsonl and data/eval/merged_haikus.jsonl contain the 1504 / 2000 and 144 / 250 good haikus for initial SFT training BEFORE formatting 
- data/train/haikus.jsonl and data/eval/haikus.jsonl contain the 1504 / 2000 and 144 / 250 good haikus for initial SFT training AFTER formatting; **these are to be used for SFT training**
- notebooks/sft_training.ipynb loads good training/evaluation haikus and performs SFT training on DistilGPT-2 