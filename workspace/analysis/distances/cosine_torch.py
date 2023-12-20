#!/usr/bin/env jupyter
"""
Calculate cosine similarity of the CRISPR profiles using GPU

Based off
https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/util.py#L31
"""
from collections.abc import Iterable
from pathlib import Path

import numpy as np
import polars as pl
import torch
from torch import Tensor, device

device = device("cuda" if torch.cuda.is_available() else "cpu")

filename = "harmonized_no_sphering_profiles"
dir_path = Path("../../profiles/")
profiles_path = dir_path / f"{filename}.parquet"


def cos_sim(a: Tensor, b: Tensor) -> Tensor:
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.

    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))


# Load Metadata
df = pl.read_parquet(profiles_path)

vals = Tensor(df.select(pl.all().exclude("^Metadata.*$")).to_numpy())

# Calculate cosine similarty
cosine_sim = cos_sim(tensor, tensor)

# Save the upper triangle compressed
linear = cosine_sim[np.triu_indices(len(cosine_sim))]
joblib.dump(linear, "cosine_joblib", compress=("lzma", 9))

# Sort by correlation
_sorted = cosine_sim.sort(axis=1)

n_vals_used = 25


def get_first_last_n(tensor: Tensor, n: int):
    return tensor[:, [range(n), range(-n - 1, -1)]].reshape(-1, 2 * n)


indices, values = [
    get_first_last_n(x, n_vals_used) for x in (_sorted.indices, _sorted.values)
]

meta = df.select(pl.col("^Metadata_.*$"))
jcp_col = "Metadata_JCP2022"
jcp_df = pl.DataFrame(
    {
        "JCP2022": np.repeat(meta.select(pl.col(jcp_col)), n_vals_used * 2).astype(
            "<U15"
        ),
        "matched_JCP2022": meta.select(pl.col(jcp_col))
        .to_series()
        .to_numpy()[indices.flatten()]
        .astype("<U15"),
        "cosine_distance": values.flatten().numpy(),
    }
)


# We save our matrix
jcp_df.write_parquet("cosine_similarity_best.parquet")

# And then proceed to add gene names (TODO incorporate NCBI ids once they are in babel)
