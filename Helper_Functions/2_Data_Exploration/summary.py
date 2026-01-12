import numpy as np
import pandas as pd


'''
# config
base_stats = ['mean','sum','size','count','std','first','last','min','max','median','skewness','kurtosis']
additional_quantiles = ['quantile_01','quantile_025','quantile_075','quantile_09']
count_duplicate = ['has_duplicate_max','has_duplicate_min','has_duplicate','count_duplicate_max','count_duplicate_min','count_duplicate']
counts = ['count_unique', 'count', 'count_above_0', 'count_below_0', 'value_count_0', 'count_near_0']
higher_order_stats = ['abs_energy','root_mean_square','sum_values','realized_volatility','realized_abs_skew','realized_skew','realized_vol_skew','realized_quarticity']
min_max_positions = ['last_location_of_maximum','first_location_of_maximum','last_location_of_minimum','first_location_of_minimum']
other_min_max = ['absolute_maximum','max_over_min']
variations = ['mean_diff','mean_abs_change','mean_change','mean_second_derivative_central','absolute_sum_of_changes']
ranges = ['variance_std_ratio','ratio_beyond_01_sigma','ratio_beyond_02_sigma','ratio_beyond_03_sigma','large_standard_deviation','range_ratio',]
peaks = ['number_peaks_2','mean_n_absolute_max_2','number_peaks_5','mean_n_absolute_max_5','number_peaks_10','mean_n_absolute_max_10',]
reoccuring_values = ['count_above_mean','count_below_mean','percentage_of_reoccurring_values_to_all_values','percentage_of_reoccurring_datapoints_to_all_datapoints','sum_of_reoccurring_values','sum_of_reoccurring_data_points','ratio_value_number_to_time_series_length',]
'''

# base stats

def mean(x):
    return np.nanmean(x)

def sum(x):
    return np.nansum(x)

def size(x):
    return len(x)

## non-missing
def count(x):
    return np.sum(~np.isnan(x))

def std(x):
    return np.nanstd(x, ddof=1)

def first(x):
    x = np.asarray(x)
    mask = ~np.isnan(x)
    return x[mask][0] if np.any(mask) else np.nan

def last(x):
    x = np.asarray(x)
    mask = ~np.isnan(x)
    return x[mask][-1] if np.any(mask) else np.nan

def min(x):
    return np.nanmin(x)

def max(x):
    return np.nanmax(x)

def median(x):
    return np.median(x)

def variance(x):
    return np.var(x)

def standard_deviation(x):
    return np.std(x)

def skewness(x):
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    return pd.Series.skew(x)

def kurtosis(x):
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    return pd.Series.kurtosis(x)

# additional_quantiles 

def quantile(x, q):
    if len(x) == 0:
        return np.NaN
    return np.quantile(x, q)

def quantile_01(x):
    return np.nanquantile(x, 0.01)

def quantile_025(x):
    return np.nanquantile(x, 0.025)

def quantile_075(x):
    return np.nanquantile(x, 0.75)

def quantile_09(x):
    return np.nanquantile(x, 0.90)

# duplicate

def has_duplicate(x):
    x = np.asarray(x)
    return x.size != np.unique(x).size

def has_duplicate_max(x):
    x = np.asarray(x)
    if x.size == 0:
        return False
    max_val = np.max(x)
    return np.sum(x == max_val) >= 2

def has_duplicate_min(x):
    x = np.asarray(x)
    if x.size == 0:
        return False
    min_val = np.min(x)
    return np.sum(x == min_val) >= 2

def count_duplicate(x):
    x = np.asarray(x)
    return int(x.size - np.unique(x).size)

def count_duplicate_max(x):
    x = np.asarray(x)
    if x.size == 0:
        return 0
    max_val = np.max(x)
    return int(np.sum(x == max_val))

def count_duplicate_min(x):
    x = np.asarray(x)
    if x.size == 0:
        return 0
    min_val = np.min(x)
    return int(np.sum(x == min_val))

# count

def count_unique(x):
    x = np.asarray(x)
    return int(np.unique(x).size)

def count(x):
    x = np.asarray(x)
    return int(x.size)

def count_above(x, t):
    x = np.asarray(x)
    if x.size == 0:
        return np.nan
    return float(np.sum(x >= t) / x.size)

def count_below(x, t):
    x = np.asarray(x)
    if x.size == 0:
        return np.nan
    return float(np.sum(x <= t) / x.size)

def count_above_mean(x):
    x = np.asarray(x)
    if x.size == 0:
        return 0
    m = np.mean(x)
    return int(np.sum(x > m))

def count_below_mean(x):
    x = np.asarray(x)
    if x.size == 0:
        return 0
    m = np.mean(x)
    return int(np.sum(x < m))


## higher order

def abs_energy(x):
    x = np.asarray(x)
    return np.nansum(x ** 2)

def root_mean_square(x):
    x = np.asarray(x)
    return np.sqrt(np.nanmean(x ** 2)) if len(x) > 0 else np.nan

def sum_values(x):
    return np.nansum(x)

def realized_volatility(x):
    x = np.asarray(x)
    return np.sqrt(np.nansum(x ** 2))

def realized_abs_skew(x):
    x = np.asarray(x)
    return np.power(np.abs(np.nansum(x ** 3)), 1 / 3)

def realized_skew(x):
    x = np.asarray(x)
    s = np.nansum(x ** 3)
    return np.sign(s) * np.power(np.abs(s), 1 / 3)

def realized_vol_skew(x):
    x = np.asarray(x)
    return np.power(np.abs(np.nansum(x ** 6)), 1 / 6)

def realized_quarticity(x):
    x = np.asarray(x)
    return np.power(np.nansum(x ** 4), 1 / 4)

def realized_quarticity(x):
    x = np.asarray(x)
    return np.power(np.nansum(x ** 4), 1 / 4)


# min-max position

def last_location_of_maximum(x):
    x = np.asarray(x)
    if len(x) == 0:
        return np.nan
    return 1.0 - np.argmax(x[::-1]) / len(x)

def first_location_of_maximum(x):
    x = np.asarray(x)
    if len(x) == 0:
        return np.nan
    return np.argmax(x) / len(x)

def last_location_of_minimum(x):
    x = np.asarray(x)
    if len(x) == 0:
        return np.nan
    return 1.0 - np.argmin(x[::-1]) / len(x)

def first_location_of_minimum(x):
    x = np.asarray(x)
    if len(x) == 0:
        return np.nan
    return np.argmin(x) / len(x)

def absolute_maximum(x):
    x = np.asarray(x)
    return np.nanmax(np.abs(x)) if len(x) > 0 else np.nan

def max_over_min(x):
    x = np.asarray(x)
    if len(x) < 2:
        return 0
    min_val = np.nanmin(x)
    if min_val == 0:
        return np.nan
    return np.nanmax(x) / min_val

# variance

def mean_diff(x):
    return np.nanmean(np.diff(x.values))

def mean_abs_change(x):
    return np.mean(np.abs(np.diff(x)))

def mean_change(x):
    x = np.asarray(x)
    return (x[-1] - x[0]) / (len(x) - 1) if len(x) > 1 else np.NaN

def mean_second_derivative_central(x):
    x = np.asarray(x)
    return (x[-1] - x[-2] - x[1] + x[0]) / (2 * (len(x) - 2)) if len(x) > 2 else np.NaN

def absolute_sum_of_changes(x):
    return np.sum(np.abs(np.diff(x)))

def root_mean_square(x):
    return np.sqrt(np.mean(np.square(x))) if len(x) > 0 else np.NaN

# range

def variance_std_ratio(x):
    y = np.var(x)
    if y != 0:
        return y/np.sqrt(y)
    else:
        return np.nan
    
def variation_coefficient(x):
    mean = np.mean(x)
    if mean != 0:
        return np.std(x) / mean
    else:
        return np.nan

def large_standard_deviation(x):
    if (np.max(x)-np.min(x)) == 0:
        return np.nan
    else:
        return np.std(x)/(np.max(x)-np.min(x))

def variation_coefficient(x):
    mean = np.mean(x)
    if mean != 0:
        return np.std(x) / mean
    else:
        return np.nan

def ratio_beyond_r_sigma(x, r):
    if x.size == 0:
        return np.nan
    else:
        return np.sum(np.abs(x - np.mean(x)) > r * np.asarray(np.std(x))) / x.size

def range_ratio(x):
    mean_median_difference = np.abs(np.mean(x) - np.median(x))
    max_min_difference = np.max(x) - np.min(x)
    if max_min_difference == 0:
        return np.nan
    else:
        return mean_median_difference / max_min_difference
    
def sum_values(x):
    if len(x) == 0:
        return 0
    return np.sum(x)

def log_return(list_stock_prices):
    return np.log(list_stock_prices).diff() 


def maximum_drawdown(series):
    series = np.asarray(series)
    if len(series)<2:
        return 0
    k = series[np.argmax(np.maximum.accumulate(series) - series)]
    i = np.argmax(np.maximum.accumulate(series) - series)
    if len(series[:i])<1:
        return np.NaN
    else:
        j = np.max(series[:i])
    return j-k

def maximum_drawup(series):
    series = np.asarray(series)
    if len(series)<2:
        return 0

    series = - series
    k = series[np.argmax(np.maximum.accumulate(series) - series)]
    i = np.argmax(np.maximum.accumulate(series) - series)
    if len(series[:i])<1:
        return np.NaN
    else:
        j = np.max(series[:i])
    return j-k


def drawdown_duration(series):
    series = np.asarray(series)
    if len(series)<2:
        return 0

    k = np.argmax(np.maximum.accumulate(series) - series)
    i = np.argmax(np.maximum.accumulate(series) - series)
    if len(series[:i]) == 0:
        j=k
    else:
        j = np.argmax(series[:i])
    return k-j

def drawup_duration(series):
    series = np.asarray(series)
    if len(series)<2:
        return 0

    series=-series
    k = np.argmax(np.maximum.accumulate(series) - series)
    i = np.argmax(np.maximum.accumulate(series) - series)
    if len(series[:i]) == 0:
        j=k
    else:
        j = np.argmax(series[:i])
    return k-j


def max_over_min(series):
    if len(series)<2:
        return 0
    if np.min(series) == 0:
        return np.nan
    return np.max(series)/np.min(series)

def mean_n_absolute_max(x, number_of_maxima = 1):
    """ Calculates the arithmetic mean of the n absolute maximum values of the time series."""
    assert (
        number_of_maxima > 0
    ), f" number_of_maxima={number_of_maxima} which is not greater than 1"

    n_absolute_maximum_values = np.sort(np.absolute(x))[-number_of_maxima:]

    return np.mean(n_absolute_maximum_values) if len(x) > number_of_maxima else np.NaN


#number of valleys = number_peaks(-x, n)
def number_peaks(x, n):
    """
    Calculates the number of peaks of at least support n in the time series x. A peak of support n is defined as a
    subsequence of x where a value occurs, which is bigger than its n neighbours to the left and to the right.
    """
    x_reduced = x[n:-n]

    res = None
    for i in range(1, n + 1):
        result_first = x_reduced > _roll(x, i)[n:-n]

        if res is None:
            res = result_first
        else:
            res &= result_first

        res &= x_reduced > _roll(x, -i)[n:-n]
    return np.sum(res)


def longest_strike_below_mean(x):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return np.max(_get_length_sequences_where(x < np.mean(x))) if x.size > 0 else 0

def longest_strike_above_mean(x):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return np.max(_get_length_sequences_where(x > np.mean(x))) if x.size > 0 else 0

def last_location_of_maximum(x):
    x = np.asarray(x)
    return 1.0 - np.argmax(x[::-1]) / len(x) if len(x) > 0 else np.NaN

def first_location_of_maximum(x):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return np.argmax(x) / len(x) if len(x) > 0 else np.NaN

def last_location_of_minimum(x):
    x = np.asarray(x)
    return 1.0 - np.argmin(x[::-1]) / len(x) if len(x) > 0 else np.NaN

def first_location_of_minimum(x):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return np.argmin(x) / len(x) if len(x) > 0 else np.NaN

# Test non-consecutive non-reoccuring values ?
def percentage_of_reoccurring_values_to_all_values(x):
    if len(x) == 0:
        return np.nan
    unique, counts = np.unique(x, return_counts=True)
    if counts.shape[0] == 0:
        return 0
    return np.sum(counts > 1) / float(counts.shape[0])

def percentage_of_reoccurring_datapoints_to_all_datapoints(x):
    if len(x) == 0:
        return np.nan
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    value_counts = x.value_counts()
    reoccuring_values = value_counts[value_counts > 1].sum()
    if np.isnan(reoccuring_values):
        return 0

    return reoccuring_values / x.size

def sum_of_reoccurring_values(x):
    unique, counts = np.unique(x, return_counts=True)
    counts[counts < 2] = 0
    counts[counts > 1] = 1
    return np.sum(counts * unique)

def sum_of_reoccurring_data_points(x):
    unique, counts = np.unique(x, return_counts=True)
    counts[counts < 2] = 0
    return np.sum(counts * unique)

def ratio_value_number_to_time_series_length(x):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    if x.size == 0:
        return np.nan

    return np.unique(x).size / x.size

def abs_energy(x):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return np.dot(x, x)

# crossing the mean ? other levels ? 
def number_crossing_m(x, m):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    # From https://stackoverflow.com/questions/3843017/efficiently-detect-sign-changes-in-python
    positive = x > m
    return np.where(np.diff(positive))[0].size

def absolute_maximum(x):
    return np.max(np.absolute(x)) if len(x) > 0 else np.NaN

def value_count(x, value):
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    if np.isnan(value):
        return np.isnan(x).sum()
    else:
        return x[x == value].size
    
def range_count(x, min, max):
    return np.sum((x >= min) & (x < max))

