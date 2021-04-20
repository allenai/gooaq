# GooAQ 🥑: Google Answers to Google Questions! 

This repository contains the code/data accompanying our recent work on long-form question answering.   

**NOTE** This dataset should not be used for any commercial purposes. See the [license](LICENSE) for the detailed terms.

## Data 
To get the data, see the [`data/`](data/) directory.
Note that the data is stored via [`git-lfs`](https://git-lfs.github.com/). 
If you're cloning the project (`git clone git@github.com:allenai/gooaq.git`), make sure to also run `git lfs pull` as well.    
 
Each row of the data file should look like this: 
```json
{
  "id": 3339543,
  "question": "what is the difference between collagen and whey protein?",
  "short_answer": null,
  "answer": "The main differences between the amino acid profiles of whey and collagen are that whey contains all 9 essential amino acids, while collagen only has 8. ... Collagen is a fibrous protein found in the skin, cartilage, and bones of animals whereas whey comes from milk.",
  "answer_type": "feat_snip"
}
```
where the questions `question` are collected via Google auto-complete.  
The answers responses (`short_answer` and `answer`) were collected from Google's answer boxes.
The answer types (`answer_type`) are inferred based on the html content of Google's response. 
Here is the dominant types in the current dataset:  
 - `feat_snip`: explanatory responses; the majoriy the question/responses are of this type. 
 - `collection`: list responses (e.g., steps to accomplish something). 
 - `knowledge`: typically short responses for knowledge seeking questions. 
 - `unit_conv`: questions about converting units. 
 - `time_conv`: questions about converting times. 
 - `curr_conv`: questions about converting currencies.  

Here are several more examples from the data: 
```json
{
  "id": 5009708,
  "question": "carbon dioxide comprises approximately what percentage of tropospheric gases?",
  "short_answer": "04%",
  "answer": "Carbon dioxide comprise approximately . 04% of tropospheric gases.",
  "answer_type": "feat_snip"
}
{
  "id": 8317711,
  "question": "what is the distance between uranus and earth?",
  "short_answer": "1.7858 billion mi",
  "answer": null,
  "answer_type": "knowledge"
}
{
  "id": 3547745,
  "question": "what is the symbol for the element aluminum?",
  "short_answer": "Al",
  "answer": null,
  "answer_type": "knowledge"
}
{
  "id": 3552841,
  "question": "what is the volume of a 12 oz can?",
  "short_answer": "340.957",
  "answer": null,
  "answer_type": "unit_conv"
}
{
  "id": 1032187,
  "question": "exajoule is how many joules?",
  "short_answer": "1e+18 Joule",
  "answer": null,
  "answer_type": "unit_conv"
}
{
  "id": 610247,
  "question": "are words that start with e?",
  "short_answer": null,
  "answer": "['eager.', 'eagle.', 'eagre.', 'eared.', 'earls.', 'early.', 'earns.', 'earth.']",
  "answer_type": "collection"
}
{
  "id": 1309258,
  "question": "how long does it take to boil a hard egg?",
  "short_answer": null,
  "answer": "['Place your eggs in a single layer on the bottom of your pot and cover with cold water. ... ', 'Over high heat, bring your eggs to a rolling boil.', 'Remove from heat and let stand in water for 10-12 minutes for large eggs. ... ', 'Drain water and immediately run cold water over eggs until cooled.']",
  "answer_type": "collection"
}
{
  "id": 2518757,
  "question": "is ways to lose weight?",
  "short_answer": null,
  "answer": "['Trying intermittent fasting. ... ', 'Tracking your diet and exercise. ... ', 'Eating mindfully. ... ', 'Eating protein for breakfast. ... ', 'Cutting back on sugar and refined carbohydrates. ... ', 'Eating plenty of fiber. ... ', 'Balancing gut bacteria. ... ', \"Getting a good night's sleep.\"]",
  "answer_type": "collection"
}
``` 
 
## Baselines 
See the scripts for reproducing our [T5](https://github.com/google-research/text-to-text-transfer-transformer/) baselines, see the [`experiments/`](experiments) directory.  

## Reproducing Human Evaluation 
TBD 

## More reading 
See the following paper: 
```bibtex 
@article{gooaq2021,
  title={GooAQ: Open Question Answering with Diverse Answer Types},
  author={Khashabi, Daniel and Ng, Amos and Khot, Tushar and Sabharwal, Ashish and Hajishirzi, Hannaneh and Callison-Burch, Chris},
  journal={arXiv preprint},
  year={2021}
}
```
