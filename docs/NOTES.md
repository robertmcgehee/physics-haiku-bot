# NOTES

This document records design decisions, observed failure modes, and lessons learned during physics haiku dataset generation/validation and the subsequent SFT of DistilGPT-2 using the curated dataset.

## Penalizing Few-Shot Cheating

During evaluation, I discovered that the few-shot base model would frequently pass the haiku checks by verbatim copying one or more lines from the example haikus included in the few-shot prompt. While this behavior is expected for a small base model, it artificially inflated syllable and haiku pass rates and did not reflect genuine haiku generation ability. To address this, I introduced an additional evaluation constraint: if a generated haiku line passes the syllable check but is an exact match to any example haiku line in the few-shot prompt, that line is marked as invalid. As a result, few-shot pass rates dropped significantly (41% 2nd-line syllables passing dropped to 1%, for example). The updated metrics in SCOREBOARD now accurately reflect true generation performance for this model rather than prompt copying.

## SFT Experiments via Data Formatting

As I comment below, I was inspired to simplify the raw data so that pre-SFT, I could choose different formats for the haiku prompts and responses. After some initial experiments that showed the SFT model performance could depend sensitively on data formatting choices, I tested the performance of 8 different SFT models on the test keywords. The only difference between the 8 models was the formatting of the otherwise-identical training/evaluation haikus. Most experiments used 'Write a haiku about <keyword>' and focused on changing how the line numbers appeared in the prompt/response. I tried using no numbers; 1), 2), 3); and <LINE1>, <LINE2>, <LINE3>. All variations had a fourth line with '<END>' in the haiku response, but I toggled its appearance in the prompt.

I discovered that switching 'Write a haiku about <keyword>' to 'Write 3 lines about Keyword: <keyword>' improved performance across haiku checks quite significantly. After more testing, the final prompt/response variation which beat out the rest and became the default format for data was "Write 3 lines about Keyword: " + keyword  + "\n1)\n2)\n3)" and "1) " + lines[0] + "\n2) " + lines[1] + "\n3) " + lines[2] + "\n<END>". 

To give a sense for the variation in model performance across these formatting choices, just a few of the experiments results appear below.

| Data Format                            | 3 Lines | Keyword | 1st Syll | 2nd Syll | 3rd Syll |
|----------------------------------------|---------|---------|----------|----------|----------|
| Write a haiku... (no numbers or <END>) |  0.00   |  0.00   |   0.14   |   0.01   |   0.00   |
| Write a haiku... (<LINE#> both <END>)  |  0.29   |  0.15   |   0.21   |   0.12   |   0.24   |
| Write 3 lines... ( #) one <END> )      |  0.89   |  0.56   |   0.20   |   0.11   |   0.19   |

## SFT Choices
- reduced learning rate from 5e-5 to 2e-5 to reduce overfitting observed in early experiments
- trained with response-only loss so only the generated haiku (and not the prompt) contributes to the training objective
- enabled early stopping based on validation loss to save GPU time while preventing model degradation
- used a small, carefully curated SFT dataset with strict structural accuracy: all training/evaluation examples pass all haiku checks
- prioritized validation loss as a coarse training diagnostic; afterwards, haiku checks on the test keywords act as the primary evaluation metric

## Training Data Simplification 

Initial experiments with supervised fine-tuning of DistilGPT-2 revealed that the original variety of prompts were not ideal for the small model to learn the expected rules for writing a haiku. For example, when prompting the SFT-trained model with the held-out test set of keywords, it produced 0 correct-syllable haikus, 0.8% of haikus with 3 lines, and 6.4% of haikus with keyword usage. At first, I tried to augment the original prompts with additional instructions for DistilGPT-2 by appending 'Rules:\n- Output exactly 3 lines.\n- Use a 5-7-5 syllable count.\n- Include the keyword exactly once.\n- Output only the haiku (no title, no extra text).' I found that this offered mixed improvement. On the test keywords, the SFT model trained on the augmented training/evaluation data did better in producing haikus with the keyword 18.4% of the time, but no longer ever produced haikus with 3 lines and still never got the syllables correct.

Since the base model is so small and it's not fine-tuned for following instructions, I decided simplifying the training/evaluation data may prove better than adding instructions. So, I reduced all prompt varieties down to a single, simple one; added line numbers to both prompt and response; and ended the response data with an <END> delimiter. An example training haiku looks like

{"prompt": "Write a haiku about force.\n1)\n2)\n3)", "response": "1) Silent pulls align\n2) force in silence bends light now\n3) Stars answer, we fall\n<END>"}

This new, simpler prompt/response format has yielded considerably better initial SFT model results: on the test set, 44% of haikus include the keyword and 4% have all correct syllables. 

To more easily permit further experimentation with improving SFT model performance by simply tweaking the *format and not the content* of the training/evaluation data, I have refactored the code so that raw training/evaluation haiku data is in its simplest form:

{"prompt_num":1,"keyword":"force","haiku":"Force steers silent mass\nAcross space it bends each path\nVector in my hand"}

This simple raw data is then checked for haiku consistency, reformatted, and written to a single JSONL file for training. The particular formatting that appears in the final training data may be easily adjusted and new training data made without the need for regenerating haikus.

I still use the 5 prompt variations when generating the data with SOTA LLMs to help produce variety in haikus. I also do not expect the final SFT-trained model to respond well to simple, semantic prompt variations since it is such a small model. For this project, I'm really trying to have the SFT model perform well when I tell it to write a haiku about ____ and give it its learned format. 

Note for posterity: I used this new, simpler format and generated an entirely new dataset. But I also reformatted the old haikus and merged the two to double the data. In the raw JSONL files, the new data appears first followed by the old data, each in prompt number order. While the bulk of the prompt body as well as the key "haiku writing task" wording was identical for both sets of data, I made some slight adjustments to prompt details when generating the newer data.

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

I set aside one novel concept family for evaluation during training and another for testing ('Cosmology' and 'Particle Physics,' respectively). Since I came up with every keyword in each concept family myself, I was able to avoid overlap between training concept family keywords and keywords from evaluation or test concept families (e.g. I withheld 'Compton scattering' from Advanced Lab to avoid leakage into Particle Physics). I also avoided overlap between evaluation and test concept family keywords. 

I did permit overlap between separate training data concept families (e.g. 'diamagnetism' in Condensed Matter overlapping with 'magnet' from Electromagnetism). In fact, I let the amount of overlap between concepts guide my selection of the training concept families, which include all 'basic' physics keywords, versus the evaluation and test concept families.

To prevent memorization and post-SFT model brittleness, I used 5 prompt variations per keyword in the training data. Each concept family has 25 keywords to create 

- 1000 training haikus 
- 125 evaluation haikus 
- 25 test keywords

## Training Data Regeneration After Validation

Once I implemented check_train_data, I was able to verify that all of the initial training haikus correctly had 3 lines and used the physics keyword once or twice. But **all 40 JSON files** (corresponding to 8 concept families x 5 prompt variations) had haikus that failed the syllable count test. In fact, **442 of the 1000 original haikus had incorrect syllable counts**. I was surprised by this poor performance by GPT-5.2 especially since all prompt variations contained explicit instructions to "Be sure to enforce a 5-7-5 syllable count." On experimenting with different prompt additions, I came to find that adding another explicit syllable-counting message at the end of the prompt would decrease the failure rate by almost a factor of 2.

In the process of checking these original haikus, I also discovered (using a small check_keywords script) that 4 of my physics keywords (['cylindrical coordinates', 'nuclear magnetic resonance', 'topological insulator', 'differential geometry']) had too many syllables to fit on a single haiku line. All things considered, it's not terrible that 4 / 200 of my keywords were faulty. Since I really want the keyword(s) in its entirety on a single line, I replaced each of these keywords.

With the new end-of-prompt wording and new keywords, I regenerated all of the training data haikus from scratch resulting in only **223/1000 bad haikus** (as compared to 442/1000). In addition, the new prompt caused 1 of the generated JSONL files to have 25 perfect haikus, a feat not seen in the original training data. 

## Training Data Generation Failure Modes

I found that checking each batch of 25 haikus quickly by eye was invaluable before proceeding with the systematic checks on each individual haiku. Out of the 40 JSONL files generated, 7 files had to be completely regenerated due to bad repetition between the individual haikus. There were two failure patterns I noticed. The easiest to spot, which happened 3 times, was all 25 haikus would have identical first and third lines, with only the second line differentiated between them in part by the physics keyword. The other failure mode was slightly less easy to detect: the third haiku line would be repeated across a small handful of the haikus. So, out of the 25 haikus, there might be about 8 different third lines repeated for instance. I found this failure in 4 / 40 files.

In each case, regenerating the impacted file with the same prompt resulted in good haikus without repetition.