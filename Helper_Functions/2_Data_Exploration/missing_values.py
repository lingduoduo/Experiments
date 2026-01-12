import pandas as pd
import numpy as np
from warnings import warn


def check_missing(df, output_path=None):
    """
    check the total number & percentage of missing values per variable of a pandas dfframe
    """

    result = pd.concat([df.isnull().sum(), df.isnull().mean()], axis=1)
    result = result.rename(index=str, columns={0: 'total missing', 1: 'proportion'})
    if output_path is not None:
        result.to_csv(output_path + 'missing.csv')
        print('result saved at', output_path, 'missing.csv')
    return result


def drop_missing(df, axis=0):
    """
    Listwise deletion:
    excluding all cases (listwise) that have missing values

    Parameters
    ----------
    axis: drop cases(0)/columns(1),default 0

    Returns
    -------
    Pandas dataframe with missing cases/columns dropped
    """

    df = df.dropna(axis=axis, inplace=False)
    return df


def add_var_denote_NA(df, NA_col=[]):
    """
    creating an additional variable indicating whether the data
    was missing for that observation (1) or not (0).
    """

    for i in NA_col:
        if df[i].isnull().sum() > 0:
            df[i + '_is_NA'] = np.where(df[i].isnull(), 1, 0)
        else:
            warn("Column %s has no missing cases" % i)

    return df


def impute_NA_with_arbitrary(df, impute_value, NA_col=[]):
    """
    replacing NA with arbitrary values.
    """


    for i in NA_col:
        if df[i].isnull().sum() > 0:
            df[i + '_' + str(impute_value)] = df[i].fillna(impute_value)
        else:
            warn("Column %s has no missing cases" % i)
    return df


def impute_NA_with_avg(df, strategy='mean', NA_col=[]):
    """
    replacing the NA with mean/median/most frequent values of that variable.
    Note it should only be performed over training set and then propagated to test set.
    """

    for i in NA_col:
        if df[i].isnull().sum() > 0:
            if strategy == 'mean':
                df[i + '_impute_mean'] = df[i].fillna(df[i].mean())
            elif strategy == 'median':
                df[i + '_impute_median'] = df[i].fillna(df[i].median())
            elif strategy == 'mode':
                df[i + '_impute_mode'] = df[i].fillna(df[i].mode()[0])
        else:
            warn("Column %s has no missing" % i)
    return df


def impute_NA_with_end_of_distribution(df, NA_col=[]):
    """
    replacing the NA by values that are at the far end of the distribution of that variable
    calculated by mean + 3*std
    """

    for i in NA_col:
        if df[i].isnull().sum() > 0:
            df[i + '_impute_end_of_distri'] = df[i].fillna(df[i].mean() + 3 * df[i].std())
        else:
            warn("Column %s has no missing" % i)
    return df


def impute_NA_with_random(df, NA_col=[], random_state=0):
    """
    replacing the NA with random sampling from the pool of available observations of the variable
    """

    for i in NA_col:
        if df[i].isnull().sum() > 0:
            df[i + '_random'] = df[i]
            # extract the random sample to fill the na
            random_sample = df[i].dropna().sample(df[i].isnull().sum(), random_state=random_state)
            random_sample.index = df[df[i].isnull()].index
            df.loc[df[i].isnull(), str(i) + '_random'] = random_sample
        else:
            warn("Column %s has no missing" % i)
    return df
