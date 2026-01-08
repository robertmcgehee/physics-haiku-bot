# Haiku Bot Evaluation Scoreboard

All models are evaluated on the test keyword set (particle physics) using a fixed generation configuration. For each keyword, the model generates a haiku which is then scored for consistency with haiku rules.

## Models on the Board

- **Base (0-shot)**  
  Vanilla `distilgpt2` prompted only with a request to write a haiku

- **Base (few-shot)**  
  `distilgpt2` with three in-context haiku examples demonstrating the desired structure

- **SFT (0-shot)**  
  `distilgpt2` fine-tuned via supervised learning on the curated dataset of physics haikus, evaluated
  without any in-context examples

## Scoreboard

![Haiku scoreboard](haiku_scoreboard.png)

### Pass Rates by Model

| Model              | lines_ok | keyword_ok | syllables_ok | haiku_ok |
|--------------------|----------|------------|---------------|----------|
| Base (0-shot)      | 0.00     | 0.00       | 0.00          | 0.00     |
| Base (few-shot)    | 0.08     | 0.00       | 0.00          | 0.00     |
| SFT (0-shot)       | 1.00     | 0.96       | 0.00          | 0.00     |

## Conclusions

- **Zero-shot prompting completely fails** for the base model
- **Few-shot prompting almost completely fails**
- **Supervised fine-tuning produces a large and consistent improvement**, but still leaves much to be desired: it doesn't get syllables correct and the actual haiku outputs are poor quality