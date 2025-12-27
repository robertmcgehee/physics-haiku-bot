# Physics Haiku Bot

## Overview

This project explores whether a small, carefully curated dataset is sufficient to fine-tune a smaller model like DistilGPT-2 to reliably generate structured creative outputs in the form of physics haikus. SOTA LLMs like GPT-5.2 have trouble reliably producing such haikus, with failure rates as high as 44% even with explicit prompting. Thus, this is no easy task for a small model to tackle.

This repository contains raw pre-SFT training data (i.e. physics haikus) prior to final filtering/merging organized by prompt template and physics concept family. The haikus were generated using ChatGPT-5.2. It also contains functions to check haikus for consistency.

## Status Note

Training data regenerated after preliminary haiku failure analysis. Merged training files with haikus which pass all checks will be implemented next.

## Key Files

- data/train/check_keywords.py checks that all physics keywords are 7 syllables or less
- data/train/promptX contains all training haikus
- data/train/train_data_prompts.py contains the exact prompts used to generate the haikus
- data/train/check_train_data.py checks all training haikus for 1) 3 lines, 2) physics keyword use, and 3) correct syllable count; prints a high-level summary; set verbose=True for more details