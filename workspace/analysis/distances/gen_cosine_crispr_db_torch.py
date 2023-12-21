#!/usr/bin/env jupyter
"""
Calculate cosine similarity of the CRISPR profiles using GPU

Based off
https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/util.py#L31
"""
from pathlib import Path

import numpy as np
import polars as pl
import torch
from broad_babel.query import run_query
from torch import Tensor, device

from utils import batch_processing, parallel

device = device("cuda" if torch.cuda.is_available() else "cpu")

assert device.type == "cuda", "Not running on GPUs"


def get_first_last_n(tensor: Tensor, n: int):
    return tensor[:, [range(n), range(-n - 1, -1)]].reshape(-1, 2 * n)


@batch_processing
def jcp_to_standard(x):
    return run_query(query=x, input_column="JCP2022", output_column="standard_key")[0][
        0
    ]


def cos_sim(a: Tensor, b: Tensor) -> Tensor:
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.

    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))


filename = "harmonized_no_sphering_profiles"
dir_path = Path("../../profiles/")
profiles_path = dir_path / f"{filename}.parquet"

# Load Metadata
df = pl.read_parquet(profiles_path)

vals = Tensor(df.select(pl.all().exclude("^Metadata.*$")).to_numpy())

# Calculate cosine similarty
cosine_sim = cos_sim(vals, vals)

# Save the upper triangle compressed
# joblib.dump(cosine_sim[np.triu_indices(len(cosine_sim))], "cosine_joblib.gz")

# Sort by correlation
_sorted = cosine_sim.sort(axis=1)

n_vals_used = 25


indices, values = [
    get_first_last_n(x, n_vals_used) for x in (_sorted.indices, _sorted.values)
]


meta = df.select(pl.col("^Metadata_.*$"))
url_col = "url"
meta = meta.with_columns(
    pl.concat_str(
        pl.col("Metadata_Source"),
        pl.col("Metadata_Plate"),
        pl.col("Metadata_Well"),
        separator="/",
    )
    .str.replace(r"^", "https://phenaid.ardigen.com/static-jumpcpexplorer/images/")
    .str.replace("$", "_1.jpg")
    .alias(url_col)
)

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
        url_col: np.repeat(meta.get_column("url"), n_vals_used * 2).astype("U"),
    }
)


# We save our matrix
jcp_df.write_parquet("cosine_similarity_best.parquet")

# And then proceed to add gene names (TODO incorporate NCBI ids once they are in babel)
uniq_jcp = jcp_df.select(pl.col("JCP2022")).to_series().unique().to_list()
mapper_values = parallel(uniq_jcp, jcp_to_standard)
mapper = {jcp: std for jcp, std in zip(uniq_jcp, mapper_values)}

jcp_translated = jcp_df.with_columns(
    pl.col("JCP2022").replace(mapper).alias("standard_key"),
    pl.col("matched_JCP2022").replace(mapper),
).rename({"matched_JCP2022": "matched_standard_key"})
matches_translated = jcp_translated.select(reversed(sorted(jcp_translated.columns)))
# .with_columns(pl.col("JCP2022").str.replace("JCP2022_", "").cast(pl.Int32))

# Add a link to one of the Ardigen images

# TODO add differentiating features when compared to their controls


final_version.write_parquet("crispr.parquet", compression="zstd")
