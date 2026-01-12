import numpy as np
from scipy.stats import stats, chisquare, chi2_contingency, fisher_exact
import matplotlib.pyplot as plt
import pandas as pd


# ----------------------------------------------------------
# 1) One-way Chi-Squared Test:Chi-Square Test for Goodness of Fit
# ----------------------------------------------------------
# Use when: comparing observed counts in categories vs. an expected distribution. 
# Example: did 3 versions get clicks according to an expected 40/30/30 split?
def chi_square_gof(observed, expected_probs):
    """
    One-way Chi-Squared Goodness-of-Fit test.

    Parameters
    ----------
    observed : array-like
        Observed counts per category.
    expected_probs : array-like
        Expected proportions per category (must sum to 1).

    Returns
    -------
    chi2 : float
        Chi-squared statistic.
    p_value : float
        p-value of the test.
    expected : np.ndarray
        Expected counts.
    """
    observed = np.asarray(observed, dtype=float)
    expected_probs = np.asarray(expected_probs, dtype=float)

    if observed.ndim != 1:
        raise ValueError("observed must be a 1D array")

    if len(observed) != len(expected_probs):
        raise ValueError("observed and expected_probs must have the same length")

    if not np.isclose(expected_probs.sum(), 1.0):
        raise ValueError("expected_probs must sum to 1")

    expected = expected_probs * observed.sum()

    chi2, p_value = chisquare(f_obs=observed, f_exp=expected)
    return chi2, p_value, expected

# observed = [420, 310, 270]
# expected_probs = [0.4, 0.3, 0.3]

# chi2, p, expected = chi_square_gof(observed, expected_probs)

# print("chi2 =", chi2)
# print("p    =", p)
# print("expected counts =", expected)


# ----------------------------------------------------------------
# 2) Chi-Square Test for Association (Contingency Table)
# ----------------------------------------------------------------
# Use when: testing independence/association between 2 categorical variables.
# Example: conversion (yes/no) differs by country (US/CA/UK)?

def chi_square_contingency(table, correction=False):
    """
    Chi-Squared test of independence for a contingency table.

    Parameters
    ----------
    table : array-like (RxC)
        Contingency table of observed counts.
    correction : bool
        Whether to apply Yates' correction (default False).

    Returns
    -------
    chi2 : float
        Chi-squared statistic.
    p_value : float
        p-value of the test.
    dof : int
        Degrees of freedom.
    expected : np.ndarray
        Expected counts under independence.
    """
    table = np.asarray(table, dtype=float)

    if table.ndim != 2:
        raise ValueError("table must be a 2D array (contingency table)")

    if np.any(table < 0):
        raise ValueError("table counts must be non-negative")

    chi2, p_value, dof, expected = chi2_contingency(
        table, correction=correction
    )
    return chi2, p_value, dof, expected
# table = [
#     [120, 880],   # US
#     [ 90, 910],   # CA
#     [ 60, 940],   # UK
# ]

# chi2, p, dof, expected = chi_square_contingency(table)

# print("chi2 =", chi2)
# print("dof  =", dof)
# print("p    =", p)
# print("expected counts:\n", expected)

# ------------------------
# 3) Fisher’s Exact Test
# ------------------------
# Use when: 2x2 contingency table, especially with small counts.
# Example: conversion differs between Control vs Treatment?
def fisher_exact_test(table, alternative="two-sided"):
    """
    Fisher's Exact Test for a 2x2 contingency table.

    Parameters
    ----------
    table : array-like (2x2)
        Contingency table of observed counts.
    alternative : str
        'two-sided', 'less', or 'greater'.

    Returns
    -------
    odds_ratio : float
        Estimated odds ratio.
    p_value : float
        p-value of the test.
    """
    table = np.asarray(table, dtype=int)

    if table.shape != (2, 2):
        raise ValueError("Fisher's Exact Test requires a 2x2 table")

    if np.any(table < 0):
        raise ValueError("table counts must be non-negative")

    odds_ratio, p_value = fisher_exact(
        table, alternative=alternative
    )
    return odds_ratio, p_value

# Rows: group (control, treatment)
# Cols: outcome (converted, not_converted)
# table_2x2 = np.array([
#     [8,  92],   # control
#     [18, 82],   # treatment
# ])

# odds_ratio, p = fisher_exact(table_2x2, alternative="two-sided")
# print("\nFisher’s Exact Test (2x2)")
# print("  odds_ratio =", odds_ratio)
# print("  p          =", p)
# Interpretation: small p => evidence of different conversion rates between groups.


def contingency_table(x, y):
    """
    Create a contingency table from two categorical variables.

    Parameters
    ----------
    x, y : array-like
        Categorical variables.

    Returns
    -------
    pd.DataFrame
        Contingency table.
    """
    return pd.crosstab(x, y)

# ------------------------------------------------
# Crosstab + Stacked Bar Chart
# Crosstab between gender and alcohol consumption
# ------------------------------------------------
gender_acl = pd.crosstab(student['gender'], student['acl'])

fig, ax = plt.subplots(figsize=(7, 4))
gender_acl.plot(kind='bar', stacked=True, ax=ax)
ax.set_title("Gender vs Alcohol Consumption")
plt.show()

# Chi-Square Test on Crosstab
chi_stat, p_value, dof, expected = stats.chi2_contingency(gender_acl)

expected_table = pd.DataFrame(
    expected,
    index=gender_acl.index,
    columns=gender_acl.columns
)

print("Chi-square statistic:", chi_stat)
print("p-value:", p_value)
print("Degrees of freedom:", dof)
print("Expected frequencies:\n", expected_table)

# ------------------------------------------------
# Chi-Square Test with Pandas + Visualization
# ------------------------------------------------
# Bar plots
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

student['gender'].value_counts().plot(
    kind='bar',
    ax=axes[0],
    title='Gender'
)

student['acl'].value_counts().plot(
    kind='bar',
    ax=axes[1],
    title='Alcohol'
)

plt.tight_layout()
plt.show()
