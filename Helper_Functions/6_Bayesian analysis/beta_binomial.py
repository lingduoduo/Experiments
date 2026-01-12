import numpy as np
from scipy.stats import beta

def beta_binomial_posterior(successes, trials, a=1.0, b=1.0, cred=0.95, grid_size=20001):
    """
    Bayesian analysis for Binomial likelihood with Beta prior.

    Model:
      p ~ Beta(a, b)
      k | p ~ Binomial(n, p)

    Posterior:
      p | k,n ~ Beta(a + k, b + n - k)

    Returns summary stats + draws and an optional grid posterior pdf.
    """
    k, n = int(successes), int(trials)
    if not (0 <= k <= n):
        raise ValueError("successes must be between 0 and trials")

    # Posterior parameters
    a_post = a + k
    b_post = b + (n - k)

    # Posterior summaries
    mean = a_post / (a_post + b_post)
    var = (a_post * b_post) / (((a_post + b_post) ** 2) * (a_post + b_post + 1))

    alpha = (1 - cred) / 2
    ci_low, ci_high = beta.ppf([alpha, 1 - alpha], a_post, b_post)

    # MAP (mode) exists only if a_post>1 and b_post>1
    if a_post > 1 and b_post > 1:
        map_est = (a_post - 1) / (a_post + b_post - 2)
    else:
        map_est = None  # boundary mode when <=1

    # Posterior draws
    draws = np.random.beta(a_post, b_post, size=50_000)

    # Grid posterior (optional; useful for plotting)
    p_grid = np.linspace(0, 1, grid_size)
    pdf_grid = beta.pdf(p_grid, a_post, b_post)

    return {
        "prior": {"a": a, "b": b},
        "data": {"successes": k, "trials": n, "failures": n - k},
        "posterior": {"a": a_post, "b": b_post},
        "mean": mean,
        "variance": var,
        "map": map_est,
        "credible_interval": (ci_low, ci_high),
        "draws": draws,
        "p_grid": p_grid,
        "pdf_grid": pdf_grid,
    }


def posterior_predictive_next_m(k, n, a=1.0, b=1.0, m=1):
    """
    Posterior predictive for future m Bernoulli trials:
      K_new | data ~ Beta-Binomial(m, a+k, b+n-k)

    Returns pmf over {0..m}.
    """
    from scipy.special import betaln, comb

    a_post, b_post = a + k, b + (n - k)
    xs = np.arange(m + 1)

    # Beta-Binomial PMF: C(m, x) * B(x+a_post, m-x+b_post) / B(a_post, b_post)
    log_pmf = (
        np.log([comb(m, x, exact=False) for x in xs]) +
        (betaln(xs + a_post, (m - xs) + b_post) - betaln(a_post, b_post))
    )
    pmf = np.exp(log_pmf)
    pmf /= pmf.sum()
    return xs, pmf


# -----------------------
# Example usage
# -----------------------
if __name__ == "__main__":
    # Data: k successes out of n trials
    k, n = 37, 50

    # Prior: Beta(a,b) (uniform prior is Beta(1,1))
    res = beta_binomial_posterior(k, n, a=2, b=2, cred=0.95)

    print("Posterior Beta(a,b):", res["posterior"])
    print("Posterior mean:", round(res["mean"], 4))
    print("Posterior MAP:", None if res["map"] is None else round(res["map"], 4))
    lo, hi = res["credible_interval"]
    print("95% credible interval:", (round(lo, 4), round(hi, 4)))

    # Posterior predictive: distribution of successes in next m trials
    xs, pmf = posterior_predictive_next_m(k, n, a=2, b=2, m=10)
    print("\nPosterior predictive for next 10 trials (k_new pmf):")
    for x, p in zip(xs, pmf):
        print(f"{x}: {p:.4f}")
