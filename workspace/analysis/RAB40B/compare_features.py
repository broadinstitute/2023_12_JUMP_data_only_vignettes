#!/usr/bin/env jupyter

# Linked issue: https://github.com/broadinstitute/2023_12_JUMP_data_only_vignettes/issues/4 apply_scaler,
# Compare the four genes of interest that have been shown as anticorrelated:
# - Cluster A:
#  - RAB40B
#  - RAB40C
# - Cluster B:
#  - INSYN1
#  - PIK3R3

from pathlib import Path

import pandas as pd  # TODO stick to polars
import polars as pl
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests

fpath = Path(
    "/dgx1nas1/storage/data/shared/morphmap_profiles/orf/full_profiles_cc_adj_mean_corr.parquet"
)
genes_of_interest = ("RAB40B", "RAB40C", "INSYN1", "PIK3R3")


df = pl.read_parquet(fpath)
sub_df = df.filter(pl.col("Metadata_Symbol").is_in(genes_of_interest))
groups = dict(
    (x, f"{'RAB40B/C' if x.startswith('RAB') else 'INS/PIK'}")
    for x in genes_of_interest
)

clusters = sub_df.with_columns(
    pl.col("Metadata_Symbol").replace(groups).alias("Metadata_Cluster")
)


medians = clusters.group_by("Metadata_Cluster").median()
diff = medians.select(pl.all().exclude("^Metadata.*$").diff())
feature_diff = diff.filter(~pl.all_horizontal(pl.all().is_null())).melt()
feature_diff.sort(by="value").write_csv("feature_diffs.csv")


cluster_a = clusters.filter(pl.col("Metadata_Cluster") == "RAB40B/C").select(
    pl.all().exclude("^Metadata.*$")
)
cluster_b = clusters.filter(pl.col("Metadata_Cluster") == "INS/PIK").select(
    pl.all().exclude("^Metadata.*$")
)
results = []
for feature in cluster_a.columns:
    cluster_A = cluster_a.get_column(feature)
    cluster_B = cluster_b.get_column(feature)

    # Use t-test or Mann-Whitney U test based on data distribution
    t_stat, p_val = stats.ttest_ind(cluster_A, cluster_B, equal_var=False)

    results.append({"Feature": feature, "T-Statistic": t_stat, "P-Value": p_val})


results_df = pd.DataFrame(results)

# drop rows with NaN
results_df = results_df.dropna()

# Apply multiple testing correction

corrected_pvals = multipletests(results_df["P-Value"], method="fdr_bh")[1]
results_df["Corrected P-Value"] = corrected_pvals

# Filter significant features
significant_features = results_df[results_df["Corrected P-Value"] < 0.05]
significant_features.to_csv("significant_features.csv")
