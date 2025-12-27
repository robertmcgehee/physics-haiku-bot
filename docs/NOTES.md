# NOTES

This document records design decisions, observed failure modes, and lessons learned during physics haiku dataset generation and validation.

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

## Training Data Regeneration After Validation

Once I implemented check_train_data, I was able to verify that all of the initial training haikus correctly had 3 lines and used the physics keyword once or twice. But **all 40 JSON files** (corresponding to 8 concept families x 5 prompt variations) had haikus that failed the syllable count test. In fact, **442 of the 1000 original haikus had incorrect syllable counts**. I was surprised by this poor performance by GPT-5.2 especially since all prompt variations contained explicit instructions to "Be sure to enforce a 5-7-5 syllable count." On experimenting with different prompt additions, I came to find that adding another explicit syllable-counting message at the end of the prompt would decrease the failure rate by almost a factor of 2.

In the process of checking these original haikus, I also discovered (using a small check_keywords script) that 4 of my physics keywords (['cylindrical coordinates', 'nuclear magnetic resonance', 'topological insulator', 'differential geometry']) had too many syllables to fit on a single haiku line. All things considered, it's not terrible that 4 / 200 of my keywords were faulty. Since I really want the keyword(s) in its entirety on a single line, I replaced each of these keywords.

With the new end-of-prompt wording and new keywords, I regenerated all of the training data haikus from scratch resulting in only **223/1000 bad haikus** (as compared to 442/1000). In addition, the new prompt caused 1 of the generated JSONL files to have 25 perfect haikus, a feat not seen in the original training data. 

## Training Data Generation Failure Modes

I found that checking each batch of 25 haikus quickly by eye was invaluable before proceeding with the systematic checks on each individual haiku. Out of the 40 JSONL files generated, 7 files had to be completely regenerated due to bad repetition between the individual haikus. There were two failure patterns I noticed. The easiest to spot, which happened 3 times, was all 25 haikus would have identical first and third lines, with only the second line differentiated between them in part by the physics keyword. The other failure mode was slightly less easy to detect: the third haiku line would be repeated across a small handful of the haikus. So, out of the 25 haikus, there might be about 8 different third lines repeated for instance. I found this failure in 4 / 40 files.

In each case, regenerating the impacted file with the same prompt resulted in good haikus without repetition.