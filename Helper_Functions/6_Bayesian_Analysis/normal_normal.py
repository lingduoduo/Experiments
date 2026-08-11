import numpy as np
from scipy.stats import norm

def normal_normal_mean(
    x,
    mu0,
    tau0,
    sigma,
    cred=0.95,
    n_draws=50_000
):
    """
    Bayesian Normal-Normal model for estimating a mean.

    Likelihood:
      x_i | mu ~ Normal(mu, sigma^2)  (sigma known)

    Prior:
      mu ~ Normal(mu0, tau0^2)

    Returns posterior distribution and summaries.
    """

    x = np.asarray(x)
    n = len(x)
    xbar = x.mean()

    # Posterior variance and mean
    tau_n2 = 1 / (1 / tau0**2 + n / sigma**2)
    mu_n = tau_n2 * (mu0 / tau0**2 + n * xbar / sigma**2)

    tau_n = np.sqrt(tau_n2)

    # Credible interval
    alpha = (1 - cred) / 2
    ci_low, ci_high = norm.ppf(
        [alpha, 1 - alpha],
        loc=mu_n,
        scale=tau_n
    )

    # Posterior draws
    draws = np.random.normal(mu_n, tau_n, size=n_draws)

    return {
        "prior": {"mu0": mu0, "tau0": tau0},
        "data": {"n": n, "xbar": xbar, "sigma": sigma},
        "posterior": {"mean": mu_n, "std": tau_n},
        "credible_interval": (ci_low, ci_high),
        "draws": draws
    }

def posterior_predictive(mu_n, tau_n, sigma, size=10_000):
    return np.random.normal(
        loc=mu_n,
        scale=np.sqrt(sigma**2 + tau_n**2),
        size=size
    )

np.random.seed(0)

# Observed data
x = np.random.normal(loc=5.0, scale=2.0, size=30)

# Prior belief about mean
mu0 = 4.0     # prior mean
tau0 = 1.5    # prior std
sigma = 2.0   # known observation std

res = normal_normal_mean(x, mu0, tau0, sigma)

print("Posterior mean:", round(res["posterior"]["mean"], 4))
print("Posterior std:", round(res["posterior"]["std"], 4))
print("95% credible interval:",
      tuple(round(v, 4) for v in res["credible_interval"]))
