import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split


def imbalance_check(X: pd.Series, y: pd.Series):
    class_counts = X.value_counts()
    class_proportions = y.value_counts(normalize=True)

    print(f"Class counts: {class_counts}")
    print(f"Class proportions: {class_proportions}")


def apply_smote(X: pd.Series, y: pd.Series, random_state: int = 42):
    """
    Apply SMOTE to balance the target variable.
    Returns resampled X and y.
    """
    smote = SMOTE(random_state=random_state)
    X_res, y_res = smote.fit_resample(X, y)
    return X_res, y_res


def split_data(X: pd.Series, y: pd.Series, test_size: float = 0.2, random_state: int = 42):
    """
    Split dataset into training and test sets.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
