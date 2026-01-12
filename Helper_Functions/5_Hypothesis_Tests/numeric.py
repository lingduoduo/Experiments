import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

def _normalize(p, eps=1e-12):
    p = np.asarray(p, dtype=float)
    p = np.clip(p, eps, None)          # avoid zeros
    return p / p.sum()                 # ensure sums to 1

def kl_divergence(p, q, eps=1e-12):
    p = _normalize(p, eps)
    q = _normalize(q, eps)
    return np.sum(p * np.log(p / q))

def jensen_shannon_divergence(p, q, eps=1e-12, base=np.e):
    """
    Jensen–Shannon Divergence is a symmetrized and smoothed variant of KL divergence, bounded between 0 and 1, which improves numerical stability and interpretability when comparing empirical distributions.
    If base=2, JSD is bounded in [0, 1].
    """
    p = _normalize(p, eps)
    q = _normalize(q, eps)
    m = 0.5 * (p + q)
    jsd = 0.5 * kl_divergence(p, m, eps) + 0.5 * kl_divergence(q, m, eps)
    if base != np.e:
        jsd /= np.log(base)
    return jsd

def jensen_shannon_distance(p, q, eps=1e-12, base=2):
    """Jensen–Shannon distance = sqrt(JSD). Often used as a metric."""
    return np.sqrt(jensen_shannon_divergence(p, q, eps=eps, base=base))

# p = [0.1, 0.2, 0.7]
# q = [0.2, 0.2, 0.6]

# print("JSD (base=2):", jensen_shannon_divergence(p, q, base=2))
# print("JS distance :", jensen_shannon_distance(p, q, base=2))


# Two-Sample Kolmogorov–Smirnov (KS) Test - sensitive to detect any distribution difference
# Distribution-free, compares entire distributions (shape + location).
def ks_test(x, y):
    """
    Two-sample Kolmogorov–Smirnov test.
    H0: x and y are drawn from the same distribution.
    """
    statistic, p_value = stats.ks_2samp(x, y)
    return statistic, p_value


# Mann–Whitney U Test - detect median shift
def mann_whitney_test(x, y, alternative="two-sided"):
    """
    Mann–Whitney U test.
    H0: x and y have the same distribution (median).
    """
    statistic, p_value = stats.mannwhitneyu(
        x, y, alternative=alternative
    )
    return statistic, p_value


# Wilcoxon Rank-Sum Test (a.k.a. Wilcoxon–Mann–Whitney) - detect median shift
def wilcoxon_rank_sum_test(x, y):
    """
    Wilcoxon rank-sum test (independent samples).
    H0: x and y have the same distribution.
    """
    statistic, p_value = stats.ranksums(x, y)
    return statistic, p_value


# x = np.random.normal(0, 1, 1000)
# y = np.random.normal(0.2, 1, 1000)

# print("KS test:", ks_test(x, y))
# print("Mann–Whitney:", mann_whitney_test(x, y))
# print("Wilcoxon rank-sum:", wilcoxon_rank_sum_test(x, y))


# Normality check (Shapiro–Wilk)
def is_normal(x, alpha=0.05):
    """
    Returns True if sample appears normally distributed.
    """
    x = np.asarray(x)
    if x.size < 3:
        return False
    _, p = stats.shapiro(x)
    return p > alpha

# Given two samples
# Both normal → Welch’s t-test, Otherwise → Mann–Whitney U (robust to skew / non-normality)
def adaptive_two_sample_test(x, y, alpha=0.05):
    """
    Chooses a two-sample test based on normality.
    Returns (test_name, statistic, p_value)
    """
    x = np.asarray(x)
    y = np.asarray(y)

    normal_x = is_normal(x, alpha)
    normal_y = is_normal(y, alpha)

    if normal_x and normal_y:
        # Welch's t-test (does NOT assume equal variance)
        stat, p = stats.ttest_ind(x, y, equal_var=False)
        return "welch_t_test", stat, p
    else:
        # Mann–Whitney U (rank-based, skew-tolerant)
        stat, p = stats.mannwhitneyu(x, y, alternative="two-sided")
        return "mann_whitney_u", stat, p


def wasserstein_distance(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    return stats.wasserstein_distance(x, y)


def kl_divergence(x, y, bins=50, eps=1e-12):
    """
    KL divergence D_KL(P || Q)
    """
    x = np.asarray(x)
    y = np.asarray(y)

    p_hist, bin_edges = np.histogram(x, bins=bins, density=True)
    q_hist, _ = np.histogram(y, bins=bin_edges, density=True)

    p = p_hist + eps
    q = q_hist + eps

    p /= p.sum()
    q /= q.sum()

    return np.sum(p * np.log(p / q))

# x = np.random.normal(0, 1, 1000)
# y = np.random.gamma(2.0, 1.0, 1000)

# print(adaptive_two_sample_test(x, y))
# print("Wasserstein:", wasserstein_distance(x, y))
# print("KL:", kl_divergence(x, y))


def lr(x, y):
    """
    Linear regression analysis for bivariate numerical data.

    Parameters
    ----------
    x : array-like
        Independent variable
    y : array-like
        Dependent variable

    Returns
    -------
    results : dict
        Dictionary containing regression results and statistics
    """

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy import stats
    import statsmodels.api as sm

    # ---------------------------
    # Prepare data
    # ---------------------------
    x = np.asarray(x)
    y = np.asarray(y)

    df = pd.DataFrame({"x": x, "y": y})

    # ---------------------------
    # Scatterplot
    # ---------------------------
    plt.figure()
    plt.scatter(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Scatterplot of x vs y")
    plt.show()

    # ---------------------------
    # Correlation
    # ---------------------------
    r, r_p = stats.pearsonr(x, y)

    # ---------------------------
    # Least-squares regression
    # ---------------------------
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()

    b0, b1 = model.params

    # ---------------------------
    # Predictions & residuals
    # ---------------------------
    y_hat = model.predict(X)
    residuals = y - y_hat

    # ---------------------------
    # Fit statistics
    # ---------------------------
    r2 = model.rsquared
    rmse = np.sqrt(np.mean(residuals ** 2))

    # ---------------------------
    # Trend line plot
    # ---------------------------
    plt.figure()
    plt.scatter(x, y, label="Observed")
    plt.plot(x, y_hat, color="red", label="Least-squares line")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Least-Squares Regression Line")
    plt.legend()
    plt.show()

    # ---------------------------
    # Residual plot
    # ---------------------------
    plt.figure()
    plt.scatter(x, residuals)
    plt.axhline(0, linestyle="--")
    plt.xlabel("x")
    plt.ylabel("Residual")
    plt.title("Residual Plot")
    plt.show()

    # ---------------------------
    # Output summary
    # ---------------------------
    print("Regression Equation:")
    print(f"ŷ = {b0:.3f} + {b1:.3f}x\n")

    print("Correlation:")
    print(f"Pearson r = {r:.3f}, p-value = {r_p:.4f}\n")

    print("Model Fit:")
    print(f"R-squared = {r2:.3f}")
    print(f"RMSE = {rmse:.3f}")
    print(f"F-statistic = {model.fvalue:.3f}, p-value = {model.f_pvalue:.4f}")

    # ---------------------------
    # Return structured results
    # ---------------------------
    return {
        "intercept": b0,
        "slope": b1,
        "correlation_r": r,
        "correlation_p": r_p,
        "r_squared": r2,
        "rmse": rmse,
        "residuals": residuals,
        "model": model
    }


# np.random.seed(0)
# x = np.linspace(0, 10, 40)
# y = 2.5 * x + np.random.normal(0, 3, size=len(x))

# results = lr(x, y)
# print(results)

