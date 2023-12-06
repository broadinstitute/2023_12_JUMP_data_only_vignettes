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
# %% [Markdown]
"""
Find correlations between CD44 and HAS2. Question inspired by Prof. Chonghui Chen from Baylor College of Medicine during ASCB2 2023.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from broad_babel.query import run_query
from utils import load_path, get_figs_dir

figs_dir = get_figs_dir()
df = load_path("../../profiles/harmonized_no_sphering_profiles.parquet")

genes_of_interest = ("CD44", "HAS2")
cd44_crispr, *cd44_orf = run_query(
    query="CD44", input_column="standard_key", output_column="JCP2022"
)[0]

gene_matches = {pert: dict() for pert in genes_of_interest}
for gene in genes_of_interest:
    crispr, *orf = list(
        map(
            lambda x: x[0],
            run_query(query=gene, input_column="standard_key", output_column="JCP2022"),
        )
    )
    gene_matches[gene]["crispr"] = crispr
    if len(orf):
        gene_matches[gene]["orf"] = orf[0]


# %% Calculate the correlations between has2 and cd44 based on CRISPR data

feat_cols = [x for x in df.columns if not x.startswith("Metadata")]
data_only = df.loc[
    df["Metadata_JCP2022"].isin([x["crispr"] for x in gene_matches.values()])
]
data_only.set_index(
    data_only["Metadata_JCP2022"].map(
        {v["crispr"]: k for k, v in gene_matches.items()}
    ),
    inplace=True,
)
for method in ("pearson", "kendall", "spearman"):
    candidates_corr = (
        data_only[feat_cols].T.corr(method=method).sort_index().sort_index(axis=1)
    )
    sns.heatmap(candidates_corr, robust=True)
    plt.tight_layout()
    plt.savefig(
        figs_dir
        / f"correlations_{method}_harmony_{'_'.join(genes_of_interest).lower() }.png",
        dpi=300,
    )
    plt.close()
