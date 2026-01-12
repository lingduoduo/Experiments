import hashlib

import pandas as pd
from collections import combinations


def generate_dummies(df, column, columns_to_drop=None, prefix=None):
    """
    One-hot transformation
    """

    dummies = pd.get_dummies(df[column], prefix=prefix)
    new_columns = list(dummies.columns)
    dummies.reset_index()
    dummies = dummies.astype("int")
    df = df.join(dummies[new_columns])
    if not columns_to_drop:
        columns_to_drop = [column]
    df = df.drop(columns_to_drop, axis=1)
    return df


def hash_and_map(feature, hash_size):
    hashed_feature = int(hashlib.sha256(str(feature).encode('utf-8')).hexdigest(), 16)
    return hashed_feature % hash_size


def generate_hashing(df, column, hash_size, columns_to_drop=None, prefix=None):
    """
    Hashing transformation
    """

    output_features = df[column].apply(lambda feature: hash_and_map(feature, hash_size))
    output_features = output_features.apply(lambda row: row.value_counts(), axis=1).fillna(0)
    if not columns_to_drop:
        columns_to_drop = [column]
    if prefix is not None:
        new_columns = [prefix + '_' + str(i) for i in range(hash_size)]
        output_features.columns = new_columns
    new_df = pd.concat([df, output_features], axis=1)
    return new_df


def count_encoding(df, column):
    counts = df[column].value_counts()
    df[f'{column}_count'] = df[column].map(counts)
    return df


def generate_count_encoding(df, column, columns_to_drop=None, prefix=None):
    """
    Count encoding transformation
    """

    output_features = df[column].apply(lambda feature: count_encoding(feature))
    if not columns_to_drop:
        columns_to_drop = [column]
    if prefix is not None:
        new_columns = [prefix + '_' + str(i) for i in range(column)]
        output_features.columns = new_columns
    new_df = pd.concat([df, output_features], axis=1)
    return new_df


def generate_cross_feature_interactions(df, features_to_cross, prefix=None):
    """
    Feature Interactions
    df = create_cross_feature_interactions(df, ["age", "gender"], "age_gender")
    df = create_cross_feature_interactions(df, ["country", "language"], "country_language")
    """

    cross_combinations = list(combinations(features_to_cross, 2))
    for feature in cross_combinations:
        new_col_name = prefix if prefix else f'{feature[0]}_{feature[1]}'
        df[new_col_name] = df[feature[0]].astype(str) + '_' + df[feature[1]].astype(str)
    return df


def generate_bucket(df, col, bucket_size=10, prefix=None):
    """
    Generate buckets by bucket size
    df = create_income_bucket(df, 'income', bucket_size=10000, prefix='income_bucket')
    """
    if prefix is None:
        prefix = f'{col}_bucket'
    bins = range(0, df[col].max() + bucket_size, bucket_size)
    labels = [f'{start}-{end - 1}' for start, end in zip(bins[:-1], bins[1:])]
    df[prefix] = pd.cut(df[col], bins=bins, labels=labels, include_lowest=True)
    return df
