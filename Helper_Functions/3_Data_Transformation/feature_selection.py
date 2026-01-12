from __future__ import annotations

from typing import Optional, Tuple, Union

import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, SelectPercentile, f_classif, RFE
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import StandardScaler


ArrayLike = Union[np.ndarray]


def select_k_best(
    X_train: ArrayLike,
    y_train: ArrayLike,
    X_test: ArrayLike,
    k: int = 2,
    *,
    score_func=f_classif,
    return_selector: bool = False,
) -> Union[Tuple[ArrayLike, ArrayLike], Tuple[ArrayLike, ArrayLike, SelectKBest]]:
    """Select top-k features using a univariate statistical test (default: ANOVA F-test)."""
    selector = SelectKBest(score_func=score_func, k=k)
    X_train_selected = selector.fit_transform(X_train, y_train)
    X_test_selected = selector.transform(X_test)
    return (X_train_selected, X_test_selected, selector) if return_selector else (X_train_selected, X_test_selected)


def select_percentile(
    X_train: ArrayLike,
    y_train: ArrayLike,
    X_test: ArrayLike,
    percentile: int = 10,
    *,
    score_func=f_classif,
    return_selector: bool = False,
) -> Union[
    Tuple[ArrayLike, ArrayLike],
    Tuple[ArrayLike, ArrayLike, SelectPercentile],
]:
    """Select top features by percentile using a univariate statistical test."""
    selector = SelectPercentile(score_func=score_func, percentile=percentile)
    X_train_selected = selector.fit_transform(X_train, y_train)
    X_test_selected = selector.transform(X_test)
    return (X_train_selected, X_test_selected, selector) if return_selector else (X_train_selected, X_test_selected)


def select_rfe(
    X_train: ArrayLike,
    y_train: ArrayLike,
    X_test: ArrayLike,
    n_features_to_select: int,
    *,
    estimator: Optional[object] = None,
    step: int = 1,
    max_iter: int = 2000,
    return_selector: bool = False,
) -> Union[Tuple[ArrayLike, ArrayLike], Tuple[ArrayLike, ArrayLike, RFE]]:
    """Recursive Feature Elimination (RFE) with a linear model by default."""
    if estimator is None:
        estimator = LogisticRegression(max_iter=max_iter)

    selector = RFE(estimator=estimator, n_features_to_select=n_features_to_select, step=step)
    X_train_selected = selector.fit_transform(X_train, y_train)
    X_test_selected = selector.transform(X_test)
    return (X_train_selected, X_test_selected, selector) if return_selector else (X_train_selected, X_test_selected)


def apply_pca(
    X_train: ArrayLike,
    X_test: ArrayLike,
    n_components: int = 2,
    *,
    whiten: bool = False,
    random_state: Optional[int] = None,
    return_transformer: bool = False,
) -> Union[Tuple[ArrayLike, ArrayLike], Tuple[ArrayLike, ArrayLike, PCA]]:
    """PCA dimensionality reduction."""
    pca = PCA(n_components=n_components, whiten=whiten, random_state=random_state)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    return (X_train_pca, X_test_pca, pca) if return_transformer else (X_train_pca, X_test_pca)


def feature_union_transform(
    X: ArrayLike,
    *,
    pca_components: int = 2,
    scale_with_std: bool = True,
):
    """
    Combine multiple transformations in parallel and concatenate outputs.
    Note: scaling raw features and PCA outputs together is sometimes redundant,
    but kept here to match your original intent.
    """
    union = FeatureUnion(
        transformer_list=[
            ("pca", PCA(n_components=pca_components)),
            ("scaler", StandardScaler(with_std=scale_with_std)),
        ]
    )
    return union.fit_transform(X)
