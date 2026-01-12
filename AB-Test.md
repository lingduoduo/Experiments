# Metrics and Experiments

## A/B Testing

### What Is A/B Testing?

A/B testing (also known as **split testing** or **bucket testing**) is a method of comparing two versions of a single variable, typically by testing a subject’s response to variant A against variant B , and determining which of the two variants is more effective. It is essentially an experiment in which two or more variants are shown to users at random, and statistical analysis is used to identify which variation performs best for a specific conversion goal.

Running an A/B test that directly compares a variation against the current experience allows you to ask focused questions about changes to your website or app and to measure the impact of those changes with data.

A/B testing removes guesswork from optimization and enables data-informed decisions—shifting conversations from *“we think”* to *“we know.”* By measuring how changes affect key metrics, you can ensure that each update drives positive results.

---

### Why You Should A/B Test

A/B testing allows individuals, teams, and organizations to make careful, measurable improvements to user experiences. It helps:
- Validate or disprove hypotheses
- Understand why certain elements influence user behavior
- Resolve disagreements using data rather than opinion

Beyond answering one-off questions, A/B testing can be used continuously to improve key metrics—such as conversion rate—over time.

**Example:**  
A B2B technology company aiming to improve lead quality and volume might test:
- Headlines  
- Visual imagery  
- Form fields  
- Calls to action (CTAs)  
- Overall page layout  

By testing one change at a time, teams can isolate which changes drive impact. Over time, multiple winning changes can be combined to demonstrate measurable improvements over the original experience.

A/B testing also strengthens the entire conversion funnel:
- Test ad copy to increase click-through rates
- Test landing pages to improve conversion
- Reduce marketing spend by optimizing each step of the funnel

Product teams can similarly use A/B testing to evaluate new features, onboarding flows, modals, and in-product experiences—provided goals and hypotheses are clearly defined.

---

### Why Not A/B testing?

- Event or seasonal driven impact. We could holdback (When the changes are not applied to a small number of users, we should see the reverse effect in this group), cohort analysis, or pre/post period A/A experiment to test the issue.
- The results may not be repeatable. Sometimes our changes will only be effective to 30% of users or have a positive effect on 30% users but negatively affect 70% users. We could do a ramp-up launch to test out this issue.
- Business effects. We may also find companies call off the launching when the engineering, or opportunity cost is relatively high, or when there’s customer support or sales issue.

Considering the following scenario:

- Missing Items / Missing Supply

Key limitation: A/B testing cannot measure demand for things that do not exist in the system.

Example: On an online course platform, users search for courses that are not offered.

Why A/B testing fails: A/B testing only compares existing variants;  If a control group does not exist, there is no control or treatment; User dissatisfaction caused by missing supply cannot be captured by any experiment. So this is a product discovery or market demand problem, not an experimentation problem.

- New Experiences Without a Clear Baseline

Key limitation: Without a stable baseline, lift measurements are ambiguous.

Example: Introducing a brand-new experience such as VIP services.

Why A/B testing fails: There is no historical or conceptual “control” experience; Control and treatment users may not be comparable; Observed differences are difficult to attribute causally.

- Behavioral Biases in New Experiences. New experiences often trigger user psychology effects that distort experimental results.

Change Aversion: Users resist unfamiliar interfaces or workflows

Initial confusion can cause short-term engagement drops

Early negative impact may not reflect long-term value

Novelty Effect

New features attract attention simply because they are new: Engagement increases temporarily; Improvements may not reflect real product quality gains.

As a result: Early A/B test results may reflect user psychology rather than true product impact.

Real word data is nasty, so do the test. Even if the test is statistically significant initially, the effect can be flattened when you ramp up the change (i.e. gradually increase the percentage of users to the new version). This is mainly because:

---

### A/B Testing Process

Below is a common framework for running A/B tests:

1. **Identify Goals**  
   Define conversion goals such as button clicks, sign-ups, purchases, or other meaningful user actions. Decide KPI metrics.

2. **Collect Data**  
   Use analytics to identify optimization opportunities. Focus on high-traffic pages, low conversion rates, or high drop-off areas to gather results faster. 

3. **Generate Hypotheses**  
   Develop hypotheses explaining why a change may improve performance. Prioritize ideas based on expected impact and implementation effort. Design experiment effects including the unit of diversion, population, size, and duration), and carry out the test.

4. **Create Variations**  
   Use A/B testing tools (e.g., Optimizely) to implement changes. This could include:
   - Changing button colors
   - Reordering elements
   - Hiding navigation
   - Custom UI modifications  
   Always QA experiments before launch.

5. **Run the Experiment**  
   Launch the test and randomly assign users to the control or variation. Track and compare interactions.

6. **Analyze Results**  
   Evaluate performance and statistical significance. Determine whether the variation outperformed the control.

7. **Iterate and Learn**  
   - If the variation wins, apply insights to other pages and continue iterating.
   - If results are neutral or negative, treat the outcome as a learning opportunity and form new hypotheses.

Regardless of the outcome, each experiment informs future optimization efforts.

---

###  Choose the Right Metrics

After we set up our goals, we need to choose the correct metrics to convert the goals to concrete measurements such as click-through probability. It can be single or multiple metrics depending on the business needs. If you chose multiple metrics, one way is to combine them with weights to form an overall evaluation criterion (OEC). The steps mentioned in this course are:

- Invariant (Sanity) Check. Before choosing the measurement metrics that will be affected by the variants, we need to make sure invariants are controlled. For example, do you have the same number of users across the two groups (population sizing)? Do they have comparable distributions across countries, languages? Ideally, we should also assign the two groups the same number of trials.

- Determine High-level Business Metrics. This usually involves discussing with domain experts to determine the best practice, such as revenues, market shares, etc. In our online learning case, click-through probability makes more business sense.

- Expand to More Detailed MetricsFirst of all, we could list the basic customer funnel and expand it with more details to better understand the data we need to collect for the metrics. In this case, we need to capture the number of unique users that moves from "exploring the site" to "create an account."

Then we determine how to summarise the metrics. In general, there are 4 ways to summarise the metrics:

- Sums and counts, e.g., Total visits to the home page:
- Distributional metrics, e.g., Average visits to the home page per day. Aggregations such as mean, median, 25th, 75th percentile, etc.
- Probabilities and rates, e.g. Click-through rates or probabilities Rates: usually used to determine whether this change is easy to find Probabilities: determine whether users like this change
- Ratios eg. Pr(revenue-generating click)/ Pr(total clicks) Any two numbers divided by each other

To choose between these 4 methods, we usually look at:

- _Distribution of the metricsP_lot a histogram of past data: if it is normal shaped distribution: choose mean or median if it is one-sided distribution: choose 25th, 75th… percentile

- Sensitivity and robustness Sensitivity: the metrics respond well to relevant changes (e.g., button size) Robustness: when irrelevant changes (e.g., site loading time) happen, the metrics do not change a lot We usually use A/A Experiments to test them out. For example, when we use the same setup of a button to test users with different loading times, the click-through probability shouldn’t vary too much (robustness). However, if we use different button sizes, the click-through probability should change accordingly (sensitivity). When new experiments are too costly, we could also do a Retrospective Analysis by looking at past data to test out similar scenarios.

---

### Unit of Diversion (Proxies of Users)

In the online course example, we want to collect the number of unique users that moves from "exploring the site" to "create an account"? So what can be considered a "unique user", or the unit to run the test? This is the question that the unit of diversion answers. The commonly used units include:

User ID, Cookies, Events such as page view, Device ID, IP address

To determine the best unit, we need to look at:

- User experience consistency. Since we don’t want the same person to see different experiment groups at different times, we need to choose the unit that can reduce this effect and get more accurate data at the same time. For example, if we choose cookies as the unit of diversion when users switch to another browser, they may be assigned to a different group.

- Variability. We also need to look at the distributions of our metrics to make sure they don’t vary too much so that the practical significance level is realistic for the metrics we choose. For some complicated metrics, the empirical variability can be very different from the analytical one. It usually happens when we observe weird distributions of our metrics or when the unit of analysis (i.e., the denominator of your analysis metrics) is different from the unit of diversion (e.g., using the user id as a unit of diversion but the page view as the unit of analysis). In such cases, we need to use the empirical variability deducted from the A/A experiment.

- Ethical issues. Security and confidentiality issues; Whether informed consent is feasible.

### Population (Target Users)

Usually we want to target the changes to specific user groups. This is called a cohort. For example, if we change the English text prompt of a button, we may only want to test the results on English speaking users.

Note that limiting the population to a cohort may need a longer time to collect sufficient data. So unless we want to increase user stability or reduce the learning effect, using a cohort is unnecessary.

- Population Size
  
The questions we need to answer regarding the size include: How many tests do we need to get statistically significant results? How do we reduce the number of tests to save time? These are the 4 parameters that will affect the sample size:

And the specific numbers can be calculated using [this calculator](https://www.evanmiller.org/ab-testing/sample-size.html).

- When to run the test? Many businesses have seasonal effects. If our tests happen to be on holidays or back to school days, the results may not be accurate. So if possible, it’s better to test the results in a comparable time.
- Duration. As there will be novelty effect and change aversion to a new version of a product, we need to give the users some time to get used to the changes to stabilize the result.
- The fraction of traffic. We may have the intuition that if the experiment runs on all the target users, the time needed to collect a sufficient amount of data would be much less. But why the common practice is to run the experiment on a small portion of the traffic instead? This is because we are unsure if there are risks in the test version or whether it will harm the user experience. For example, if we are testing a new version of a database, we don’t want it to fail pervasively. By doing so, we could also reduce the effect of variabilities, such as holidays or weekends. Not to mention that the learning effect takes time for users to react normally.

---

### Sample Ratio Sanity Check

Single Metric

Hypothesis test and sign test are commonly used to calculate the statistical significance for a single metric. Let’s see the examples：

![img](https://towardsdatascience.com/wp-content/uploads/2020/11/1A5tTgibkVwuA87oc3KXu5g.png)

Hypothesis test: Suppose we have the following data and parameters that already passed the sanity check:

![img](https://towardsdatascience.com/wp-content/uploads/2020/11/1Qu7DXr8lsalmp3yxI3-rsw.png)

Unlike what we’ve done in the sanity check, we use the pooled probability (overall probability) as the centre of the confidence interval for a better estimation than 0.5 this time. The standard error should also be pooled:

![img](https://towardsdatascience.com/wp-content/uploads/2020/11/138jSPYmuARqkinPH2mwoDQ.png)

Following the same steps in the sanity check, we could get the result:

If the lower boundary of the confidence interval is higher than the minimum practical significance level, it is safe to recommend a launch of the experiment version.

Sign Test: Suppose when we segment the data into different days, 9 out of 14 days the control group has a higher click-through probability.

If there’s no difference between the two groups, the hypothetical probability of "success" should be 0.5. We could then use this calculator to get the two-sided P-value. We could see that the two-tail P-value is 0.424, which is much larger than 0.05 for a 95% confidence interval. So the sign test suggests there’s no statistically significant difference.

---

### Simpson’s Paradox 

If the tests do not agree with each other, we might consider Simpson's Paradox, which is a statistical phenomenon that a trend appears in the combined data, but disappears or reverses when the data are partitioned into several different groups.

!["Simpsons Paradox Animation" by Pace~svwiki licensed under CC BY-SA 4.0](https://towardsdatascience.com/wp-content/uploads/2020/11/08bMJSiKhwF1Eeq3x.gif)

Multiple Metrics

One key difference between single and multiple metrics is that:

- The more metrics you test, the more likely you see statistically significant results by chance – Multiple Comparison Controversy

This is because the probability of false-positives at least occur once would be higher.

Assume we have 3 metrics all with a false-positive probability of 5%, the chance of having at least 1 statistically significant results is 1–0.95³=0.143. When we have 20 metrics, the probability becomes 1–0.95²⁰=0.642.

Luckily, it is not repeatable. If we do the test again or segment it into small groups, it should disappear.

We could also use these techniques to resolve the multiple comparison issue:

How to resolve multiple comparison controversy?

The general solution is to use a higher confidence interval. This can be achieved by:

a) Assuming independence, and set only the overall alpha Then we use:αᵒᵛᵉʳᵃˡˡ = 1-(1 – αᶦⁿᵈᶦᵛᶦᵈᵘᵃˡ) ⁿ to calculate individual α.

b) Bonferroni Correction This method has no assumptions. It calculates the individual α by αᶦⁿᵈᶦᵛᶦᵈᵘᵃˡ = αᵒᵛᵉʳᵃˡˡ/number of metrics. Note that this is a relatively conservative method, you may miss some valuable observations.

c) Familywise Error Rate The FER only controls the probability that any metric shows a false positive.

d) Control False Discovery Rate In this case, we allow a high probability of false positive, as long as there isn’t too many. Note that FDR should be used when the number of metrics is very large, usually hundreds.

---

### Detect Network Bias Effects

Consider the following bias cases...
One friend is targeted for an experiment that gives her a better messaging experience. I am not targeted, and my messaging experience doesn’t change. However, her better messaging experience causes her to spend more time on the site and send more messages, including some to me. I then respond to her, and spend more time on the site as well. What happened here? The fact that my friend received a new feature had an impact on me, even though I was not part of the experiment. 

In short, interference can bias the results of an A/B test to the point where it can lead to the wrong decision. For example, one could conclude that a new relevance algorithm has no impact (and stop investing in its development) when it in fact has a positive impact through the network that has simply gone unmeasured. Or, one could think a feature has a positive impact when it’s actually negative. For example, it is not uncommon to see low-quality “viral” content have positive engagement effects on users, but have a negative overall impact. If it’s not worth re-sharing, it has low (or sometimes negative) network effects and decreases the quality of the conversation overall. 

LinkedIn Method: The key intuition is that if there is no network effect, both of these experiments should give us the same estimated effect. So cluster the LinkedIn graph into 10,000 clusters. The graph comprises all active LinkedIn members as nodes and their “connections” as edges. We then split these clusters into two parallel experiments:

A) An individual-level experiment, where members are sorted randomly into treatment or control groups.
B) A cluster-based experiment, where a whole cluster (i.e., community) of users is either in treatment or in control. In other words, if I am treated, a significant proportion of my connections are also treated. If I am part of the control group, a significant proportion of my connections are also under control.


