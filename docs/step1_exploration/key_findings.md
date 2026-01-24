## Key EDA Findings

The exploratory analysis surfaces several patterns that will shape the downstream feature engineering and segmentation
steps.  These findings are derived from the sample dataset but illustrate the types of behavioural signals present in
TravelTide’s data.

1. **Engagement heterogeneity** – Customers vary dramatically in how often and how intensively they use the platform.  A subset of users logs many short sessions (quick price checks), whereas another subset spends longer browsing and clicking through multiple pages.  This heterogeneity suggests that a single reward strategy will be insufficient.

2. **Discount affinity** – Users who receive or interact with discounts tend to have higher base fares.  Their sessions show elevated page click counts, implying that they actively search for deals.  These patterns motivate features measuring discount affinity (e.g., proportion of sessions with a discount flag) and support the hypothesis that “cost optimisers” represent a distinct segment.

3. **Trip type differentiation** – Preliminary inspection of flight and hotel attributes (available in the enriched session table) indicates differences between users who book multi‑city journeys versus those who book simple round trips.  Multi‑city itineraries are associated with longer session durations and greater price dispersion.  This insight justifies including trip‑structure features in the customer feature table.

4. **Outlier behaviour** – A small number of sessions exhibit extremely long durations or unusually high page click counts.  Rather than dropping entire users, these sessions are flagged and either Winsorised or excluded during aggregation.  The outlier policy is transparent and documented, ensuring reproducibility and fairness.

5. **Cohort cleanliness** – After filtering on the cohort date range and removing invalid IDs, the sample cohort retains high data quality with low missingness on behavioural fields.  Demographic fields remain sparsely populated and are therefore not used in the modelling features to maintain GDPR compliance.

These findings inform the design of features in Step 2 and provide qualitative evidence for later segment profiling.
