from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """return distinct train and test sets"""
    return train_test_split(df, random_state=0, test_size=0.2)


def ungroup(X: pd.DataFrame, w: pd.DataFrame) -> pd.DataFrame:
    """expand all repeated columns"""
    #     return X.reindex(X.index.repeat(w))
    return X.loc[np.repeat(X.index.values, w)]


def group(X: pd.DataFrame, w: pd.DataFrame) -> pd.DataFrame:
    """append weight to pandas dataframe by group by all columns"""
    return X.groupby(list(X.columns)).size().to_frame(w).reset_index()


def split_weighting_data(X: pd.DataFrame,
                         y: pd.Series,
                         w: str = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """transform the data"""
    X = X.assign(y=y)
    if w is not None:
        X_train, X_test = split(ungroup(X, w))
        return group(X_train), group(X_test)
    else:
        X[w] = 1
        return split(X)
