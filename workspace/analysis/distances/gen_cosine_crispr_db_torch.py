#!/usr/bin/env jupyter
"""
Calculate cosine similarity of the CRISPR profiles using GPU,
then wrangle information and produce an explorable data frame.

The GPU section is based off this function
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
checkpoint_path = Path("jcp_df.parquet")

# Set names
jcp_col = "Metadata_JCP2022"  # Name of columns in input data frames
url_col = "example_image_standard_key"
match_url_col = "example_image_match"
url_prefix = "https://phenaid.ardigen.com/static-jumpcpexplorer/images/"
url_suffix = "_1.jpg"

# Load Metadata
df = pl.read_parquet(profiles_path)

if checkpoint_path.exists():
    jcp_df = pl.read_parquet(checkpoint_path)
else:
    vals = Tensor(df.select(pl.all().exclude("^Metadata.*$")).to_numpy())

    # Calculate cosine similarty
    cosine_sim = cos_sim(vals, vals)

    # Sort by correlation
    _sorted = cosine_sim.sort(axis=1)

    n_vals_used = 25

    indices, values = [
        get_first_last_n(x, n_vals_used) for x in (_sorted.indices, _sorted.values)
    ]

    # Add a link to one of the Ardigen images
    meta = df.select(pl.col("^Metadata_.*$"))
    meta = meta.with_columns(
        pl.concat_str(
            pl.col("Metadata_Source"),
            pl.col("Metadata_Plate"),
            pl.col("Metadata_Well"),
            separator="/",
        )
        .str.replace(r"^", url_prefix)
        .str.replace("$", url_suffix)
        .alias(url_col)
    )

    jcp_df = pl.DataFrame(
        {
            "JCP2022": np.repeat(meta.select(pl.col(jcp_col)), n_vals_used * 2).astype(
                "<U15"
            ),
            "match_JCP2022": meta.select(pl.col(jcp_col))
            .to_series()
            .to_numpy()[indices.flatten()]
            .astype("<U15"),
            "cosine_distance": values.flatten().numpy(),
            url_col: np.repeat(meta.get_column("url"), n_vals_used * 2).astype("U"),
            match_url_col: list(
                map(
                    lambda x: url_prefix + "/".join(x) + url_suffix,
                    meta.select(
                        pl.col(["Metadata_Source", "Metadata_Plate", "Metadata_Well"])
                    ).to_numpy()[indices.flatten()],
                )
            ),
        }
    )

    jcp_df.write_parquet("cosine_similarity_best.parquet", compression="zstd")

# And then proceed to add gene names (TODO incorporate NCBI ids once they are in babel)
uniq_jcp = jcp_df.select(pl.col("JCP2022")).to_series().unique().to_list()
mapper_values = parallel(uniq_jcp, jcp_to_standard)
mapper = {jcp: std for jcp, std in zip(uniq_jcp, mapper_values)}

jcp_translated = jcp_df.with_columns(
    pl.col("JCP2022").replace(mapper).alias("standard_key"),
    pl.col("match_JCP2022").replace(mapper),
).rename({"match_JCP2022": "match_standard_key"})
matches_translated = jcp_translated.select(reversed(sorted(jcp_translated.columns)))
# .with_columns(pl.col("JCP2022").str.replace("JCP2022_", "").cast(pl.Int32))


final_output = "crispr.parquet"
matches_translated.write_parquet(final_output, compression="zstd")


# Upload to zenodo
# Automated uploads are not working
# https://github.com/zenodo/zenodo/issues/2506

"""
from os.path import expanduser
import requests
with open(expanduser("~") + "/.zenodo") as f:
    for line in f.readlines():
        name, access_token = line.strip("\n").split(": ")

params = {"access_token": access_token}
bucket_url = "https://zenodo.org/api/files/9ffb1b5b-1e3c-4618-ad91-36255e87b57e"
headers = {"Content-Type": "application/json"}
with open(final_output, "rb") as fp:
    r = requests.post(
        f"{bucket_url}?access_token={params['access_token']}",
        data=fp,
        headers=headers,
        params=params,
    )


depos_url =  "https://zenodo.org/api/deposit/depositions/10416605"
depos=requests.get(depos_url,params=params)
new = requests.post(depos.json()["links"]["newversion"], params=params, headers={"Accept": "application/json" ,**headers})

d = r.post(depos_url.json(""))
curl -X POST-H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" https://sandbox.zenodo.org/api/deposit/depositions/165/actions/newversion

"""

"""
Future plans:
- Add example of matched profile
- Find a way to compress URLs for easier visualisation
- TODO add differentiating features when compared to their controls
"""
