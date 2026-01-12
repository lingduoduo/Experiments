import numpy as np
from scipy.stats import norm, t

# -----------------------------
# 1) Population proportion CI
# -----------------------------

def ci_proportion_normal(k, n, conf=0.95):
    """
    Wald (normal approx) CI for a population proportion p.
    Works best when n is large and p not too close to 0/1.
    """
    if n <= 0 or not (0 <= k <= n):
        raise ValueError("Require n>0 and 0<=k<=n")
    phat = k / n
    z = norm.ppf(0.5 + conf / 2)
    se = np.sqrt(phat * (1 - phat) / n)
    lo, hi = phat - z * se, phat + z * se
    return {"p_hat": phat, "ci": (max(0.0, lo), min(1.0, hi)), "method": "wald"}


def ci_proportion_wilson(k, n, conf=0.95):
    """
    Wilson score CI for a population proportion p.
    Generally recommended over Wald.
    """
    if n <= 0 or not (0 <= k <= n):
        raise ValueError("Require n>0 and 0<=k<=n")
    phat = k / n
    z = norm.ppf(0.5 + conf / 2)
    z2 = z * z
    denom = 1 + z2 / n
    center = (phat + z2 / (2 * n)) / denom
    half = (z / denom) * np.sqrt((phat * (1 - phat) / n) + (z2 / (4 * n * n)))
    lo, hi = center - half, center + half
    return {"p_hat": phat, "ci": (max(0.0, lo), min(1.0, hi)), "method": "wilson"}


# ------------------------------------
# 2) Population mean CI (daily metrics)
# ------------------------------------

def ci_mean_from_daily(daily_values, conf=0.95, use_t=True):
    """
    CI for the population mean using daily metric values (each day = one observation).

    - If use_t=True: uses t-interval (recommended, sigma unknown).
    - If use_t=False: uses z-interval (assumes known sigma; rarely true in practice).
    """
    x = np.asarray(daily_values, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 2:
        raise ValueError("Need at least 2 daily values for a mean CI.")

    mean = x.mean()
    s = x.std(ddof=1)
    se = s / np.sqrt(n)

    if use_t:
        crit = t.ppf(0.5 + conf / 2, df=n - 1)
        method = "t"
    else:
        crit = norm.ppf(0.5 + conf / 2)
        method = "z"

    lo, hi = mean - crit * se, mean + crit * se
    return {
        "mean": mean,
        "n_days": n,
        "std": s,
        "se": se,
        "ci": (lo, hi),
        "method": method,
    }


# -----------------------------------------------------------
# 3) Daily metrics → confidence bounds for a RATE/proportion
# -----------------------------------------------------------
# Example: daily conversion rate = conversions / visits per day.
# If you want a CI for the overall proportion over the full window,
# aggregate k=sum(conversions), n=sum(visits) and use Wilson CI.

def ci_rate_from_daily_counts(daily_successes, daily_trials, conf=0.95, method="wilson"):
    """
    Computes CI for an overall proportion using daily counts:
      k = sum(successes_d), n = sum(trials_d)
    """
    k = int(np.nansum(daily_successes))
    n = int(np.nansum(daily_trials))
    if method == "wald":
        return ci_proportion_normal(k, n, conf=conf)
    elif method == "wilson":
        return ci_proportion_wilson(k, n, conf=conf)
    else:
        raise ValueError("method must be 'wald' or 'wilson'")


# -----------------------------------------------------------
# 4) Rolling confidence bounds (monitoring daily metrics)
# -----------------------------------------------------------

def rolling_ci_mean(daily_values, window=7, conf=0.95):
    """
    Rolling CI bounds for the mean over a moving window of days.
    Returns arrays aligned to the input with NaNs for the first window-1 days.
    """
    x = np.asarray(daily_values, dtype=float)
    n = len(x)
    lo = np.full(n, np.nan)
    hi = np.full(n, np.nan)
    mid = np.full(n, np.nan)

    for i in range(window - 1, n):
        chunk = x[i - window + 1 : i + 1]
        res = ci_mean_from_daily(chunk, conf=conf, use_t=True)
        mid[i] = res["mean"]
        lo[i], hi[i] = res["ci"]

    return mid, lo, hi


def rolling_ci_rate(daily_successes, daily_trials, window=7, conf=0.95, method="wilson"):
    """
    Rolling CI bounds for a proportion/rate over a moving window using aggregated counts.
    """
    s = np.asarray(daily_successes, dtype=float)
    n = np.asarray(daily_trials, dtype=float)
    L = len(s)
    lo = np.full(L, np.nan)
    hi = np.full(L, np.nan)
    phat = np.full(L, np.nan)

    for i in range(window - 1, L):
        k = int(np.nansum(s[i - window + 1 : i + 1]))
        tot = int(np.nansum(n[i - window + 1 : i + 1]))
        res = ci_rate_from_daily_counts([k], [tot], conf=conf, method=method)
        phat[i] = res["p_hat"]
        lo[i], hi[i] = res["ci"]

    return phat, lo, hi


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # A) Proportion CI (single snapshot)
    k, n = 245, 1000
    print(ci_proportion_wilson(k, n, conf=0.95))

    # B) Mean CI using daily metric values (e.g., daily revenue per user)
    daily_revenue_per_user = [1.2, 1.0, 1.4, 0.9, 1.1, 1.3, 1.25, 1.05, 1.6, 1.15]
    print(ci_mean_from_daily(daily_revenue_per_user, conf=0.95))

    # C) Rate CI using daily counts (e.g., conversions / visits)
    daily_conv = [30, 28, 35, 27, 32, 31, 29]
    daily_visits = [1200, 1150, 1300, 1100, 1250, 1230, 1180]
    print(ci_rate_from_daily_counts(daily_conv, daily_visits, conf=0.95, method="wilson"))

    # D) Rolling bounds (7-day window)
    mean_mid, mean_lo, mean_hi = rolling_ci_mean(daily_revenue_per_user, window=5, conf=0.95)
    print("Rolling mean CI last:", mean_mid[-1], (mean_lo[-1], mean_hi[-1]))

    rate_mid, rate_lo, rate_hi = rolling_ci_rate(daily_conv, daily_visits, window=3, conf=0.95)
    print("Rolling rate CI last:", rate_mid[-1], (rate_lo[-1], rate_hi[-1]))
