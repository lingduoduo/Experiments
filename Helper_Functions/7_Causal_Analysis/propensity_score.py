import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import statsmodels.formula.api as smf

np.random.seed(42)

# --------------------------------
# Estimate causal effect
# --------------------------------

n = 1000
X1 = np.random.normal(size=n)
X2 = np.random.normal(size=n)

# Treatment assignment depends on X1 and X2
logit = 0.8 * X1 - 0.5 * X2
p = 1 / (1 + np.exp(-logit))
T = np.random.binomial(1, p)

# True causal treatment effect = 2.0
Y = 2.0 * T + 1.5 * X1 + 0.5 * X2 + np.random.normal(size=n)

df = pd.DataFrame({
    "X1": X1,
    "X2": X2,
    "T": T,
    "Y": Y
})

# -------------------------
# Estimate propensity score
# P(T=1 | X)
# -------------------------
model = LogisticRegression()
model.fit(df[["X1", "X2"]], df["T"])

df["propensity"] = model.predict_proba(
    df[["X1", "X2"]]
)[:, 1]

# -------------------------
# Inverse Probability Weighting
# -------------------------
df["weight"] = np.where(
    df["T"] == 1,
    1 / df["propensity"],
    1 / (1 - df["propensity"])
)

# -------------------------
# Estimate causal effect
# -------------------------
treated = df[df["T"] == 1]
control = df[df["T"] == 0]

treated_mean = np.average(
    treated["Y"],
    weights=treated["weight"]
)

control_mean = np.average(
    control["Y"],
    weights=control["weight"]
)

ate = treated_mean - control_mean
print("Estimated ATE:", ate)


# --------------------------------
# Difference-in-Differences (DiD) 
# --------------------------------
df = pd.DataFrame({
    "group": ["control", "control", "treatment", "treatment"],
    "period": ["before", "after", "before", "after"],
    "purchase_rate": [0.20, 0.25, 0.22, 0.35]
})

# Binary variables
df["treatment"] = (df["group"] == "treatment").astype(int)
df["post"] = (df["period"] == "after").astype(int)

# Interaction term
df["treatment_post"] = df["treatment"] * df["post"]
print(df)

control_change = 0.25 - 0.20
treatment_change = 0.35 - 0.22

did = treatment_change - control_change
print(did)
