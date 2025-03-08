# Template Kit for RAMP challenge

[![Build status](https://github.com/ramp-kits/template-kit/actions/workflows/test.yml/badge.svg)](https://github.com/ramp-kits/template-kit/actions/workflows/test.yml)

## Introduction

Describe the challenge, in particular:

- Where the data comes from?
- What is the task this challenge aims to solve?
- Why does it matter?

## Getting started

### Install

To run a submission and the notebook you will need the dependencies listed
in `requirements.txt`. You can install install the dependencies with the
following command-line:

```bash
pip install -U -r requirements.txt
```

If you are using `conda`, we provide an `environment.yml` file for similar
usage.

### Challenge description

Get started on this RAMP with the
[dedicated notebook](template_starting_kit.ipynb).



## Data Preparation Tasks

- **Join the Tables**: Combine the four tables using the `Num_Acc` identifier.
- **Handle Missing Values**: Convert `-1` codes to appropriate missing value representations.
- **Feature Engineering**:
  - Calculate age from birth year and accident year.
  - Extract time features (hour, day of week, month, season).
  - Create geographic clusters using latitude and longitude.
  - Derive speed-related features from authorized speed and road characteristics.

## Modeling Approach

- **Problem Type**: Multi-class classification
- **Potential Algorithms**:
  - Random Forest
  - Gradient Boosting
  - Neural Networks
  - Support Vector Machines
- **Evaluation Metrics**:
  - Accuracy
  - F1-score (weighted)
  - Confusion Matrix
  - ROC-AUC (one-vs-rest)
- **Considerations**:
  - Class imbalance (fatal accidents typically less frequent)
  - Feature importance analysis to identify key risk factors

## Potential Insights

This analysis could help identify:

- High-risk road configurations
- Weather and visibility conditions associated with severe outcomes
- Vehicle types and characteristics linked to different injury severities
- Driver/passenger behaviors that increase accident severity
- Effectiveness of safety equipment in reducing injury severity



### Test a submission

The submissions need to be located in the `submissions` folder. For instance
for `my_submission`, it should be located in `submissions/my_submission`.

To run a specific submission, you can use the `ramp-test` command line:

```bash
ramp-test --submission my_submission
```

You can get more information regarding this command line:

```bash
ramp-test --help
```

### To go further

You can find more information regarding `ramp-workflow` in the
[dedicated documentation](https://paris-saclay-cds.github.io/ramp-docs/ramp-workflow/stable/using_kits.html)



## Acknowledgements

Data source: French BAAC (Bulletin d'Analyse des Accidents Corporels) dataset, which records all bodily injury accidents in France.

