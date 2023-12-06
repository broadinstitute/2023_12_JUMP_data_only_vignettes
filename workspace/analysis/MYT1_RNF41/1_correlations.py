#!/usr/bin/env jupyter
#!/usr/bin/env jupyter
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from broad_babel.query import run_query
from matplotlib.ticker import MaxNLocator

dataset_filepath = Path("../profiles/harmonized_no_sphering_profiles.parquet")
figs_dir = Path("../figs")
figs_dir.mkdir(exist_ok=True)

df = pd.read_parquet(dataset_filepath)

myt1_crispr, orf = [
    x[0]
    for x in run_query(
        query="MYT1", input_column="standard_key", output_column="JCP2022"
    )
]
rnf41_crispr = run_query(
    query="RNF41", input_column="standard_key", output_column="JCP2022"
)[0][0]


# %% Calculate the correlations of myt1 and rnf41
# They were reported to interact by collaborators, and Ardigen found them to correlate

feat_cols = [x for x in df.columns if not x.startswith("Metadata")]
data_only = df.loc[df["Metadata_JCP2022"].isin([myt1_crispr, rnf41_crispr])]
data_only.set_index(
    data_only["Metadata_JCP2022"].map({rnf41_crispr: "rnf41", myt1_crispr: "myt1"}),
    inplace=True,
)
for method in ("pearson", "kendall", "spearman"):
    candidates_corr = (
        data_only[feat_cols].T.corr(method=method).sort_index().sort_index(axis=1)
    )
    sns.heatmap(candidates_corr)
    plt.tight_layout()
    plt.savefig(figs_dir / f"correlations_{method}_harmony_myt1_rnf42.png", dpi=300)
    plt.close()

# %%

averaged = df.groupby("Metadata_JCP2022")[feat_cols].mean()
corr = averaged.T.corr()

myt1_correlated = corr.loc[myt1_crispr]

# %% Plot the correlations and thresholds
sns.set_style("white")
sns.set_context("talk")
ax = sns.lineplot(data=myt1_correlated.sort_values())
ax.set(xticklabels=[])
ax.spines[["right", "top"]].set_visible(False),
plt.title("Gene of interest: MYT1")
plt.xlabel("Genes ranked by correlation")
ax.set_ylabel("Pearson correlation")
ax.vlines(
    [100, len(myt1_correlated) - 100],
    ymin=-1,
    ymax=1,
    color="xkcd:dull red",
    linestyles="dashed",
)


def arrow(ax, x, y, direction):
    return ax.arrow(
        x,
        y,
        800 * direction,
        0,
        length_includes_head=True,
        color="black",
        head_width=0.1,
        head_length=300,
    )


arrow(ax, 6700, 0.92, 1)
arrow(ax, 1300, -0.87, -1)
ax.xaxis.set_major_locator(MaxNLocator(16))
plt.tight_layout()
plt.savefig(figs_dir / "scatter_ranked.png", dpi=300)
plt.close()

# %%


best_matches = [*myt1_correlated.index[:100], *myt1_correlated.index[-100:]]

best_matches_df = averaged.loc[[myt1_crispr, *best_matches]]

matches_std = best_matches_df.std().sort_values(ascending=False)

# %%

sns.set_style("white")
sns.set_context("talk")
# ax = sns.lineplot(data=matches_std.iloc[:300], color="xkcd:sky blue")
ax = sns.lineplot(data=matches_std.iloc[:300], color="xkcd:sky blue")
ax.set(xticklabels=[])
ax.spines[["right", "top"]].set_visible(False),
plt.title("Feature variability of matched genes")
plt.xlabel("Features ranked by variability")
ax.set_ylabel("Normalised variability")

ax.vlines(
    [30],
    ymin=matches_std.min(),
    ymax=matches_std.max(),
    color="xkcd:dull red",
    linestyles="dashed",
)
plt.savefig(figs_dir / "ranked_features.png", dpi=300)
plt.close()
