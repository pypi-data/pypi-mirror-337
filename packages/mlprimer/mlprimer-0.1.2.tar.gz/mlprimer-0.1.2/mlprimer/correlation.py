import pandas as pd
from scipy.stats import pointbiserialr, chi2_contingency

def check_correlation(data: pd.DataFrame, target_var: str) -> pd.DataFrame:
    """
    Evaluates feature-target correlation using point-biserial for numerical
    and chi-squared for categorical variables.
    """
    corr_results = {}
    for col in data.columns:
        if col == target_var:
            continue

        feature_data = data[col]
        target_data = data[target_var]

        if feature_data.dtype in ["int64", "float64"]:
            corr_value, p_value = pointbiserialr(target_data, feature_data)
            corr_results[col] = {
                "test_method": "pointbiserialr",
                "statistic": corr_value,
                "p_value": p_value,
                "significant": p_value < 0.05
            }

        elif feature_data.dtype == 'object':
            contingency = pd.crosstab(target_data, feature_data)
            chi2, p_value, _, _ = chi2_contingency(contingency)
            corr_results[col] = {
                "test_method": "chi2",
                "statistic": chi2,
                "p_value": p_value,
                "significant": p_value < 0.05
            }

        else:
            corr_results[col] = {"test_method": "unsupported"}

    return pd.DataFrame(corr_results).T
