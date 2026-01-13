# Haiku Bot Evaluation Scoreboard

All models are evaluated on the test keyword set (particle physics) using a fixed generation configuration. For each keyword, the model generates 8 haikus which are then scored for consistency with haiku rules.

## Models on the Board

- Base (0-shot)
  DistilGPT-2 prompted only with a request to write a haiku

- Base (few-shot) 
  DistilGPT-2 with three in-context haiku examples demonstrating the desired structure

- SFT (0-shot)  
  DistilGPT-2 fine-tuned via supervised learning on the curated dataset of physics haikus, evaluated
  without any in-context examples

## Conclusions Up Front

- the few-shot base model 'passes' current haiku checks by cheating; robust implementations of the checks coming soon and will drastically reduce (if not eliminate) all of this model's 'success'
- supervised fine-tuning produces a large and consistent improvement over both the zero-shot and few-shot base models
- SFT does still leave much to be desired: it doesn't get syllables perfect and the actual haiku outputs are poor quality

## Scoreboard

![Haiku scoreboard](haiku_scoreboard.png)

### Pass Rates by Model

| Model              | 3 Lines | Keyword | 1st Syll | 2nd Syll | 3rd Syll | Haiku pass |
|--------------------|---------|---------|----------|----------|----------|------------|
| Base (0-shot)      |  0.00   |  0.00   |   0.00   |   0.00   |   0.00   |    0.00    |
| Base (few-shot)    |  0.19   |  0.02   |   0.33   |   0.41   |   0.24   |    0.06    |
| SFT (0-shot)       |  0.89   |  0.56   |   0.20   |   0.11   |   0.19   |    0.00    |

## Remarks

It's no surprise that zero-shot prompting completely fails for the base model. What is surprising is that few-shot prompting seems to do okay at first glance. In fact, it looks like the few-shot base model is *better* than the SFT model at counting syllables! What's going on!?

A quick look at the few-shot base model's test haikus reveals the answer: when it gets syllables correct, it's often verbatim copying an example haiku in its first 3 lines. It's also still passing the 3-line check because it's inserting <END> on line 4. These sneaky check hacks are not mimicked by the SFT model. Robust checks for the few-shot model's output is coming soon. So, the few-shot model's 'successes' are actually almost complete failures. As an example, here's the raw output of a typical passing haiku verbatim (with spacing / numbering):

'1) Force bends the path in
    2) Vectors pull through quiet air
    3) Motion holds its course
      <END>
    Example 3    Write 3 lines about Keyword: symmetry
1)
2)
3'

Let's compare this to a near-perfect haiku from the SFT model:

'Equivalence keeps
2) parity is the same
3) Sets the rules
<END>'

This correctly outputs 3 lines, correctly includes the keyword 'parity', and isn't too far off on the syllable counts.