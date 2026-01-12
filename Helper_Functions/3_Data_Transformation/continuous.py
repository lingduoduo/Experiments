import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, QuantileTransformer, FunctionTransformer, PowerTransformer, PolynomialFeatures, KBinsDiscretizer


def log_transform(df, cols=[]):
    """
    Logarithmic transformation
    """

    for i in cols:
        df[i + '_log'] = np.log(df[i] + 1)
    return df


def reciprocal_transform(df, cols=[]):
    """
    Reciprocal transformation
    """

    for i in cols:
        df[i + '_reciprocal'] = 1 / (df[i])
    return df


def square_root_transform(df, cols=[]):
    """
    square root transformation
    """

    for i in cols:
        df[i + '_square_root'] = (df[i]) ** (0.5)
    return df


def exp_transform(df, coef, cols=[]):
    """
    exp transformation
    """

    for i in cols:
        df[i + '_exp'] = (df[i]) ** coef
    return df


def standardization(df, col):
    ss = StandardScaler().fit(df[col])
    df[col + '_zscore'] = ss.transform(df[[col]])
    return df


def min_max_score(df, col):
    mms = MinMaxScaler().fit(df[col])
    df[col + '_minmax_score'] = mms.transform(df[[col]])
    return df


def robust_score(df, col):
    rs = RobustScaler().fit(df[col])
    df[col + '_robust_score'] = rs.transform(df[[col]])
    return df


def quantile_score(df, col):
    transformer = QuantileTransformer(output_distribution='uniform')
    df[col + '_quantile_score'] = transformer.transform(df[[col]])
    return df    


def custom_func(X):
    return np.log1p(X)
def function_transform(df, col):
    transformer = FunctionTransformer(func=custom_func, validate=True)
    df[col + '_func_score'] = transformer.fit_transform(df[[col]])
    return df


def function_transform(df, col):
    transformer = PowerTransformer(method='yeo-johnson')
    df[col + '_power_score'] = transformer.fit_transform(df[[col]])
    return df

def polynomial_transform(df, col):
    transformer = PolynomialFeatures(degree=2, include_bias=False)
    df[col + '_polynomial_score'] = transformer.fit_transform(df[[col]])
    return df

def kBinsDiscretizer_transform(df, col):
    transformer = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
    df[col + '_kbins_score'] = transformer.fit_transform(df[[col]])
    return df

