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
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from broad_babel.query import run_query
from copairs.compute import pairwise_cosine

dataset_filepath = (
    Path("..") / ".." / "profiles" / "harmonized_no_sphering_profiles.parquet"
)
figs_dir = Path("../figs")
figs_dir.mkdir(exist_ok=True)

df = pd.read_parquet(dataset_filepath)

genes_of_interest = ("RNF41", "MYT1")
# cd44_crispr = run_query(query="CD44", input_column="standard_key", output_column="*")

gene_matches = {pert: dict() for pert in genes_of_interest}
for gene in genes_of_interest:
    results = list(
        map(
            lambda x: x,
            run_query(query=gene, input_column="standard_key", output_column="*"),
        )
    )
    for pert_type in ("crispr", "orf"):
        result_array = [x[1] for x in results if x[0] == pert_type]
        if len(result_array):
            gene_matches[gene][pert_type] = result_array[0]


# %% Calculate the correlations of myt1 and rnf41
# They were reported to interact by collaborators, and Ardigen found them to correlate

feat_cols = [x for x in df.columns if not x.startswith("Metadata")]
translator_crispr_jump_gene = {v["crispr"]: k for k, v in gene_matches.items()}
subset = df.loc[df["Metadata_JCP2022"].isin(translator_crispr_jump_gene)]
subset.set_index(
    subset["Metadata_JCP2022"].map(translator_crispr_jump_gene),
    inplace=True,
)

data_subset_no_features = subset[feat_cols]
n_samples = len(subset)
all_pair_ixs = np.array(list(product(range(n_samples), range(n_samples))))
cosine_distance = pairwise_cosine(
    data_subset_no_features.values, all_pair_ixs, batch_size=min(200, n_samples)
).reshape((n_samples, n_samples))
cosine_df = (
    pd.DataFrame(
        data=cosine_distance,
        index=subset.index,
        columns=subset.index,
    )
    .sort_index(axis=0)
    .sort_index(axis=1)
)
sns.heatmap(
    cosine_df,
    robust=True,
)
plt.tight_layout()
plt.savefig(
    figs_dir / f"heatmap_cosdist_harmony_{'_'.join(genes_of_interest).lower() }.png",
    dpi=300,
)
plt.close()
