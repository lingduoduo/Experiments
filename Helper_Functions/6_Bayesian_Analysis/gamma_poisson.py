import numpy as np
from scipy.stats import gamma

def poisson_gamma_posterior(counts, alpha=1.0, beta=1.0, exposure=None, cred=0.95, n_draws=50_000):
    """
    Bayesian analysis for Poisson count data with Gamma prior.

    Model:
      y_i ~ Poisson(lambda * t_i)   (t_i = exposure; default 1)
      lambda ~ Gamma(alpha, beta)   (shape alpha, rate beta)

    Posterior:
      lambda | y ~ Gamma(alpha + sum(y), beta + sum(t))

    Returns posterior summaries + posterior draws.
    """
    y = np.asarray(counts, dtype=float)
    if exposure is None:
        t = np.ones_like(y)
    else:
        t = np.asarray(exposure, dtype=float)
        if len(t) != len(y):
            raise ValueError("exposure must be same length as counts")
        if np.any(t < 0):
            raise ValueError("exposure must be nonnegative")

    sum_y = float(np.nansum(y))
    sum_t = float(np.nansum(t))

    a_post = alpha + sum_y
    b_post = beta + sum_t  # rate

    # Posterior mean/var for lambda
    mean = a_post / b_post
    var = a_post / (b_post ** 2)

    # Credible interval for lambda
    q = (1 - cred) / 2
    ci_low = gamma.ppf(q, a=a_post, scale=1 / b_post)
    ci_high = gamma.ppf(1 - q, a=a_post, scale=1 / b_post)

    # MAP (mode) exists if a_post > 1
    map_est = (a_post - 1) / b_post if a_post > 1 else None

    draws = np.random.gamma(shape=a_post, scale=1 / b_post, size=n_draws)

    return {
        "prior": {"alpha": alpha, "beta": beta},  # beta is RATE
        "data": {"sum_y": sum_y, "sum_t": sum_t, "n": len(y)},
        "posterior": {"alpha": a_post, "beta": b_post},
        "mean": mean,
        "variance": var,
        "map": map_est,
        "credible_interval": (ci_low, ci_high),
        "draws": draws
    }

# counts = [3, 0, 2, 5, 1, 4]  # events per day
# res = poisson_gamma_posterior(counts, alpha=1, beta=1)

# print("Posterior mean lambda:", res["mean"])
# print("95% CI:", res["credible_interval"])

def poisson_posterior_predictive(res, t_new=1.0, n_sims=50_000):
    """
    Sample posterior predictive counts y_new for exposure t_new.
    """
    lam_draws = res["draws"][:n_sims]
    return np.random.poisson(lam=lam_draws * t_new)

# y_new = poisson_posterior_predictive(res, t_new=1.0)
# print("Predicted mean count next day:", y_new.mean())
# print("95% predictive interval:", np.quantile(y_new, [0.025, 0.975]))


def compare_two_poisson_rates(yA, tA, yB, tB, alpha=1.0, beta=1.0, n_draws=200_000):
    """
    Compare two Poisson rates using independent Gamma priors.
    Returns posterior for each rate and probability that rateA > rateB.
    """
    resA = poisson_gamma_posterior([yA], alpha=alpha, beta=beta, exposure=[tA], n_draws=n_draws)
    resB = poisson_gamma_posterior([yB], alpha=alpha, beta=beta, exposure=[tB], n_draws=n_draws)

    a = resA["draws"]
    b = resB["draws"]

    prob_A_gt_B = float(np.mean(a > b))
    rate_ratio_draws = a / b
    rr_ci = tuple(np.quantile(rate_ratio_draws, [0.025, 0.975]))

    return {
        "A": resA,
        "B": resB,
        "P(rateA > rateB)": prob_A_gt_B,
        "rate_ratio_mean": float(np.mean(rate_ratio_draws)),
        "rate_ratio_95ci": rr_ci
    }

# A: 120 errors over 1,000,000 requests
# B: 95 errors over 1,000,000 requests
# cmp_res = compare_two_poisson_rates(120, 1_000_000, 95, 1_000_000)

# print("P(rateA > rateB):", cmp_res["P(rateA > rateB)"])
# print("Rate ratio 95% CI:", cmp_res["rate_ratio_95ci"])
