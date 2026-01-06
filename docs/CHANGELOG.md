# CHANGELOG

## [Unreleased]

- SFT training of DistilGPT-2 on haiku training/evaluation data using Hugging Face Trainer API

## [0.0.4] 01/06/26

- Added eval/eval_data_prompts.py and generated haikus for evaluation data
- Adopted a simplified format for all raw haiku data
- Doubled number of training/evaluation haikus 
- Combined all raw haikus by physics concept family; deleted extraneous promptX/ subfolders
- Refactored scripts to work with new raw haiku format
- Added train/format_haikus.py (adds formatted 'prompt' and 'response' key-value pairs before SFT training)

## [0.0.3] 12/29/25

- Merged all 777 good training haikus into a single JSONL file

## [0.0.2] 12/27/25

- Regenerated all training haikus with modified prompts and 4 keyword replacements
- Added check_keywords.py
- Added check_train_data.py
- Improved haiku pass rate from 442/1000 failures to 223/1000