# mlprimer
![CI](https://github.com/Kingkong2408/mlprimer/actions/workflows/ci.yml/badge.svg)


`mlprimer` is a Python package that assists with early-stage machine learning workflows. It helps users perform data profiling, feature correlation testing, preprocessing with class balancing, model training, and evaluation across common classifiers.

## Features

- Generate summary statistics from cleaned datasets
- Identify meaningful feature-target relationships
- Apply SMOTE to handle class imbalance
- Compare baseline classification models
- Perform hyperparameter tuning with GridSearch and RandomizedSearch

## Installation

### 📦 From GitHub (direct)
```bash
pip install git+https://github.com/Kingkong2408/mlprimer.git
```
### 📦 From PyPI
```bash
pip install mlprimer
```


## Usage

```python
from mlprimer import (
    calculate_summary,
    check_correlation,
    apply_smote,
    split_data,
    train_models,
    evaluate_models
)

# Summary
summary = calculate_summary(df)

# Correlation
correlation = check_correlation(df, target="target_column")

# Preprocessing
X_res, y_res = apply_smote(X, y)
X_train, X_test, y_train, y_test = split_data(X_res, y_res)

# Modeling
models = train_models(X_train, y_train)
results = evaluate_models(models, X_test, y_test)
print(results)
```

## Development Goals

- Add support for regression models
- Include more preprocessing tools (e.g., imputation, encoding helpers)
- Improve pipeline integration and configuration support

## License
MIT
