# A/B Testing & Experiments

## 1. What Is an A/B Test?

## A/B Testing Overview

A/B testing examines user experience through **randomized experiments with two variants**.  
The typical workflow includes the following steps:

1. **Determine evaluation metrics and experiment goals**
2. **Select a significance level** \( \alpha \) **and statistical power** \( 1 - \beta \)
3. **Calculate the required sample size** per variation
4. **Randomly assign users** to control and treatment groups
5. **Measure and analyze results** using appropriate statistical tests

- **Two variants** → A/B tests  
- **More than two variants** → A/B/N tests  
- Also known as:
  - Controlled experiments  
  - Randomized controlled experiments  
  - Split tests  

**Goal:**  
Make **data-driven decisions** based on results that are **reliable** and **repeatable**.

Randomized controlled experiments are considered the **gold standard** for establishing causality.

---

## 2. Experiment Workflow

1. Prerequisites  
2. Experiment Design  
3. Running the Experiment  
4. Results → Decision  
5. Post-launch Monitoring  

---

## 3. Experiment Prerequisites

### 3.1 Define Key Metrics
- Define an **Overall Evaluation Criterion (OEC)**

### 3.2 Changes Should Be Easy to Make
- Complex changes increase risk and noise  
- Example: redesigning an entire website may be too difficult to test cleanly

### 3.3 Sufficient Randomization Units
- Randomization unit = *who* or *what* is randomly assigned
- Typically requires **thousands of units**
- Larger sample sizes enable detection of **smaller effects**

---

## 4. Experiment Design

### 4.1 Population Selection
- Specific population vs. all users

### 4.2 Experiment Size
The required sample size depends on:
- Significance level \( \alpha \)
- Statistical power \( \beta \)
- **Minimum Detectable Effect (MDE)**
The smallest meaningful increase over the baseline that the experiment aims to reliably detect.

### Overall Evaluation Criterion (OEC)
A **quantitative measure** representing the experiment’s primary objective.  
Often used when **short-term and long-term metrics are correlated**.

## Multivariate Testing
- Compares **three or more variants** or combinations
- Requires **larger sample sizes** than standard A/B tests

## Bonferroni Correction
When running **n statistical tests**, adjust each test’s significance level to:

### 4.3 Experiment Duration
Consider:
- Seasonality  
- Day-of-week effects  
- Primacy and novelty effects  

---

## 5. Running Experiments

### 5.1 Data Collection
- Instrument logging
- Use company experimentation platforms

---

## 6. From Results to Decisions

- Analyze and interpret results carefully  
- This is where data scientists typically spend the most time  


### Decision Considerations
- Trade-offs between metrics (e.g., engagement ↑ vs revenue ↓)
- Cost of launching a change:
  - Engineering maintenance
  - Opportunity cost


## Network Effects
Network effects occur when outcomes are influenced by interactions across users or groups.

### Detecting Group Interference
- Split the population into **distinct clusters**
- Randomly assign half of the clusters to:
   * Control group **A₁**
   * Treatment group **B₁**
- Randomize the remaining half at the **user level** into:
   * Control group **A₂**
   * Treatment group **B₂**
- If network effects exist, results across these tests will differ

### Mitigation Strategies
- Randomize users by:
  - Time
  - Cluster
  - Geographic location


## Sequential Testing
Allows **early stopping** of experiments by setting statistical decision boundaries based on the **Type I error rate**.

⚠️ **Caution**  
If decision boundaries are crossed prematurely, the experiment may be stopped too early, leading to:
- Inflated p-values
- Incorrect conclusions


## Cohort Analysis
Analyzes **specific user groups over time** to determine whether:
- Novelty effects
- Primacy effects  

are influencing observed behavior

---

## 7. Sanity Checks

- **Pass** → continue analysis  
- **Fail** → discard results and investigate root causes  

When costs are:
- **High** → benefits must outweigh costs; set practical significance thresholds  
- **Low** → launch any positive changes  

Always consider **long-term effects**, which may differ from short-term gains.

---

## 8. Data Peeking

### What Is Data Peeking?
Stopping an experiment early because:
- Metrics improve
- p-value < 0.05

**Problem:** Results become **inaccurate** and **non-reproducible**.

### Why It Happens
- Multiple metrics
- Multiple treatment groups
- Segmenting populations
- Parallel A/B tests
- Multiple experiment iterations

### Best Practice
- Run experiments **as long as designed**

---

## 9. Multiple Testing & Metric Control

### Two-Step Rule of Thumb
1. Group metrics into:
   - Expected to be impacted
   - Possibly impacted
   - Unlikely to be impacted
2. Apply **tiered significance levels**

Example:
- Group 1 → α = 0.05  
- Group 2 → α = 0.01  
- Group 3 → α = 0.001  

---

## 10. Sample Ratio Mismatch (SRM)

### Definition
Observed control/treatment ratio deviates from design.

Example:
- Design: 1.0  
- Observed: 1.01  
- p-value < 0.05 → unlikely under correct randomization

### Causes
- Bugs in assignment logic
- Ramping experiments
- Parallel tests
- Dynamic segmentation
- Data processing pipelines

### Debugging Checklist
- Upstream of randomization point
- Variant assignment
- Data filtering (bots, fraud)
- Population segmentation

---

## 11. Violation of SUTVA

**SUTVA (Stable Unit Treatment Value Assumption):**
- Units are independent
- No interference between units

### Violations
- Social networks (e.g., Facebook, LinkedIn)
- Two-sided markets (e.g., Uber, Lyft)

### Mitigation
- Predict interference
- Isolate units
- Monitor and quantify effects

---

## 12. Novelty & Primacy Effects

- Users may overuse features initially (novelty)
- Or underuse due to resistance (primacy)

### Solution
- Monitor usage over time
- Filter novelty/primacy effects when evaluating impact

---

## 13. Underpowered Experiments

### Symptoms
- No statistically significant result
- Insufficient randomization units
- Overestimated sample size assumptions

### What To Do
- Ensure sufficient statistical power
- Continue or rerun the experiment

---

## Key Principle

> The goal of A/B testing is **reproducibility**.  
Stopping experiments prematurely undermines causal inference.


### Disclaimer
This repository and its contents are collected and shared solely for academic and research purposes. All code, data, and related materials are intended to support independent study, experimentation, and learning.

If you believe any part of this repository inadvertently includes content that should not be shared publicly or may cause concern, please contact me immediately. I will review and, if necessary, remove the material without delay.

I do not claim ownership of any third-party data or content and have made every effort to respect intellectual property and privacy rights.

