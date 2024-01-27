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

import polars as pl

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
