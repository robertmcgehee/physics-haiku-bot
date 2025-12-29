# Physics Haiku Bot

## Overview

This project explores whether a small, carefully curated dataset is sufficient to fine-tune a smaller model like DistilGPT-2 to reliably generate structured creative outputs in the form of physics haikus. SOTA LLMs like GPT-5.2 have trouble reliably producing such haikus, with failure rates as high as 44% even with explicit prompting. Thus, this is no easy task for a small model to tackle.

This repository contains SFT training data (i.e. physics haikus in prompt/response JSONL). The raw haikus are organized by prompt template and physics concept family and criteria-passing, good haikus are all merged into a single training data JSONL. The haikus were generated using ChatGPT-5.2. This repo also contains functions to check haikus for consistency, merge good haikus, and other helper functions used to generate initial haiku prompts.

## Status Note

Merged all good training haikus which pass all checks into a single JSONL file. Initial SFT training of DistilGPT-2 next.

## Key Files

- data/train/check_keywords.py checks that all physics keywords are 7 syllables or less
- data/train/train_data_prompts.py contains the exact prompts used to generate the haikus
- data/train/promptX contains all unfiltered, raw training haikus
- data/train/check_train_data.py checks all training haikus for 1) 3 lines, 2) physics keyword use, and 3) correct syllable count; prints a high-level summary; set verbose=True for more details
- data/train/merge_train_data.py checks all training data haikus pre-SFT and saves all good haikus to a single, merged .jsonl file
- data/train/good_train_haikus.jsonl contains the 777 / 1000 good haikus for initial SFT training 