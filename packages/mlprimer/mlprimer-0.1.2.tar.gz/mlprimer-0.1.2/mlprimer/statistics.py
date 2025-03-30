import pandas as pd
import numpy as np
from scipy.stats import shapiro

def mean(x):
    return sum(x) / len(x)

def median(x):
    sorted_lst = sorted(x)
    mid = len(sorted_lst) // 2
    if len(sorted_lst) % 2 == 0:
        return (sorted_lst[mid - 1] + sorted_lst[mid]) / 2
    else:
        return sorted_lst[mid]

def check_normal(x):
    return shapiro(x).pvalue >= 0.05

def calculate_summary(data: pd.DataFrame) -> pd.DataFrame:
    desc_stat = {}
    for variable in data.columns:
        variable_data = data[variable]
        variable_dict = {}

        if variable_data.dtype in ["int64", "float64"]:
            variable_dict = {
                "dtype": variable_data.dtype,
                "len": len(variable_data),
                "len_unique": variable_data.nunique(),
                "max": variable_data.max(),
                "min": variable_data.min(),
                "mean": mean(variable_data),
                "median": median(variable_data),
                "std": np.std(variable_data),
                "var": np.var(variable_data),
                "NAs": variable_data.isnull().any(),
                "normal": check_normal(variable_data)
            }

        elif variable_data.dtype == 'object':
            variable_dict = {
                "dtype": variable_data.dtype,
                "len": len(variable_data),
                "len_unique": variable_data.nunique(),
                "values": variable_data.unique().tolist(),
                "NAs": variable_data.isnull().any()
            }

        else:
            variable_dict = {"dtype": "unsupported"}

        desc_stat[variable] = variable_dict

    return pd.DataFrame(desc_stat).T
