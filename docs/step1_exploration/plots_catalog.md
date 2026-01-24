## EDA Plots Catalogue

The EDA pipeline automatically generates a series of charts to visualise data quality, distributions and
relationships.  This catalogue documents the purpose of each figure and where to find it in the artifact
directory.  Replace `<run_id>` and `<timestamp>` with the identifiers from your pipeline run.

| Plot file name                    | Description                                                                           | Example path |
|-----------------------------------|---------------------------------------------------------------------------------------|-------------|
| `missingness_overview.svg`        | Bar chart showing the percentage of missing values for each column in `sessions_clean`. | `artifacts/runs/<run_id>/step1_eda/<timestamp>/assets/missingness_overview.svg` |
| `session_duration_hist.svg`       | Histogram of session durations (seconds) highlighting the long right tail.              | `artifacts/runs/<run_id>/step1_eda/<timestamp>/assets/session_duration_hist.svg` |
| `page_clicks_hist.svg`            | Histogram of page click counts per session.                                            | `artifacts/runs/<run_id>/step1_eda/<timestamp>/assets/page_clicks_hist.svg` |
| `base_fare_hist.svg`              | Distribution of flight base fares (where available) on a log scale.                     | `artifacts/runs/<run_id>/step1_eda/<timestamp>/assets/base_fare_hist.svg` |
| `discount_rate_hist.svg`          | Distribution of discount amounts or percentages offered during sessions.                | `artifacts/runs/<run_id>/step1_eda/<timestamp>/assets/discount_rate_hist.svg` |
| `correlation_heatmap.svg`         | Correlation matrix of numeric features to identify highly correlated variables.         | `artifacts/runs/<run_id>/step1_eda/<timestamp>/assets/correlation_heatmap.svg` |
| `scatter_duration_vs_clicks.svg`  | Scatter plot showing the relationship between session duration and page clicks.         | `artifacts/runs/<run_id>/step1_eda/<timestamp>/assets/scatter_duration_vs_clicks.svg` |

Depending on the data schema and configuration, additional charts (e.g., distribution of trip types, flight durations,
or hotel nights) may be produced.  All assets reside under the `assets/` subdirectory of the Step 1 artifact run folder.
