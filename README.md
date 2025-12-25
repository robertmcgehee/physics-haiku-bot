# Physics Haiku Bot

This project explores whether a small, carefully curated dataset is sufficient to fine-tune a smaller model like DistilGPT-2 to reliably generate structured creative outputs in the form of physics haikus.

This repository currently contains unfiltered, pre-SFT training data (i.e. physics haikus) organized by prompt template and physics concept family. The haikus were generated using ChatGPT-5.2 with the exact prompts shown in data/train/train_data_prompts.py.

Sanity checks (5-7-5 syllables, line count, keyword usage) and merged training files will be added in subsequent commits.

## Training Data Choices

There do not exist thousands of discrete, separate topics in physics, so coming up with ~1,000 physics haikus for training data is non-trivial. In order to prevent the fine-tuned model from regurgitating a haiku it saw in its training data during evaluation or test time, I have created all physics keywords myself and organized them by 'concept family.' The training data keywords come from 8 concept families:
- Classical Mechanics
- Electromagnetism
- Quantum Mechanics
- Thermodynamics & Statistical Mechanics
- Mathematical Methods
- Advanced Lab
- Condensed Matter
- Relativity

I set aside one novel concept family for evals and another for testing ('Cosmology' and 'Particle Physics,' respectively). Since I came up with every keyword in each concept family myself, I was able to avoid overlap between training concept family keywords and keywords from eval or test concept families (e.g. I withheld 'Compton scattering' from Advanced Lab to avoid leakage into Particle Physics). I also avoided overlap between eval and test concept family keywords. 

I did permit overlap between separate training data concept families (e.g. 'diamagnetism' in Condensed Matter overlapping with 'magnet' from Electromagnetism). In fact, I let the amount of overlap between concepts guide my selection of the training concept families, which include all 'basic' physics keywords, versus the eval and test concept families.

To prevent memorization and post-SFT model brittleness, I used 5 prompt variations per keyword in the training data. Each concept family has 25 keywords to create 

- 1000 training haikus 
- 125 evaluation keywords 
- 125 test keywords