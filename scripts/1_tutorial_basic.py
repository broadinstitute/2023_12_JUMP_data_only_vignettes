#!/usr/bin/env jupyter
# ---
# title: Basic JUMP data access
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# This is a tutorial on how to access profiles from the [JUMP Cell Painting datasets](https://github.com/jump-cellpainting/datasets).
# We will use polars to fetch the data frames lazily, with the help of `s3fs` and `pyarrow`.
# We prefer lazy loading because the data can be too big to be handled in memory.

# %% Imports
import polars as pl
from pyarrow.dataset import dataset
from s3fs import S3FileSystem

# %% [markdown]
# The shapes of the available datasets are:
#
# a) `cpg0016-jump[crispr]`: CRISPR knockouts genetic perturbations.
# a) `cpg0016-jump[orf]`: Overexpression genetic perturbations.
# a) `cpg0016-jump[compound]`: Chemical perturbations.
#
# Their explicit location is determined by the transformations that produce the datasets.
# The aws paths of the dataframes are built from a prefix below:

# %% Paths
INDEX_FILE = "https://raw.githubusercontent.com/jump-cellpainting/datasets/50cd2ab93749ccbdb0919d3adf9277c14b6343dd/manifests/profile_index.csv"

# %% [markdown]
# We use a version-controlled csv to release the latest corrected profiles

# %%
profile_index = pl.read_csv(INDEX_FILE)
profile_index.head()

# %% [markdown]
# We do not need the 'etag' (used to check file integrity) column nor the 'interpretable' (i.e., before major modifications)

# %%
selected_profiles = profile_index.filter(
    pl.col("subset").is_in(("crispr", "orf", "compound"))
).select(pl.exclude("etag"))
filepaths = dict(selected_profiles.iter_rows())
print(filepaths)

# %% [markdown]
# We will lazy-load the dataframes and print the number of rows and columns

# %%
info = {k: [] for k in ("dataset", "#rows", "#cols", "#Metadata cols", "Size (MB)")}
for name, path in filepaths.items():
    data = pl.scan_parquet(path)
    n_rows = data.select(pl.len()).collect().item()
    schema = data.collect_schema()
    metadata_cols = [col for col in schema.keys() if col.startswith("Metadata")]
    n_cols = schema.len()
    n_meta_cols = len(metadata_cols)
    estimated_size = int(round(4.03 * n_rows * n_cols / 1e6, 0))  # B -> MB
    for k, v in zip(info.keys(), (name, n_rows, n_cols, n_meta_cols, estimated_size)):
        info[k].append(v)

pl.DataFrame(info)

# %% [markdown]
# Let us now focus on the `crispr` dataset and use a regex to select the metadata columns.
# We will then sample rows and display the overview.
# Note that the collect() method enforces loading some data into memory.

# %%
data = pl.scan_parquet(filepaths["crispr"])
data.select(pl.col("^Metadata.*$").sample(n=5, seed=1)).collect()

# %% [markdown]
# The following line excludes the metadata columns:

# %%
data_only = data.select(pl.all().exclude("^Metadata.*$").sample(n=5, seed=1)).collect()
data_only

# %% [markdown]
# Finally, we can convert this to `pandas` if we want to perform analyses with that tool.
# Keep in mind that this loads the entire dataframe into memory.

# %%
data_only.to_pandas()
