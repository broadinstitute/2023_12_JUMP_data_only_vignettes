#!/usr/bin/env jupyter
# ---
# title: Basic JUMP data access
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# This is a tutorial on how to access JUMP-Cellpainting data.
# We will use polars to fetch the data frame lazily, with the help of s3fs and pyarrow.
# We prefer lazy loading because the data can be too big to be handled in memory.

# %% Imports
import polars as pl
from pyarrow.dataset import dataset
from s3fs import S3FileSystem

# %% [markdown]
# The shapes of the available datasets are:
#
# a) crispr: Knock-out genetic perturbations.
# a) orf: Overexpression genetic perturbations.
# a) compounds: Chemical genetic perturbations.
#
# Their explicit location is determined by the transformations that producet the datasets.
# The aws paths of the dataframes are built from a prefix below:

# %% Paths
_PREFIX = (
    "s3://cellpainting-gallery/cpg0016-jump-assembled/source_all/workspace/profiles"
)
_RECIPE = "jump-profiling-recipe_2024_a917fa7"

transforms = (
    (
        "CRISPR",
        "profiles_wellpos_cc_var_mad_outlier_featselect_sphering_harmony_PCA_corrected",
    ),
    ("ORF", "profiles_wellpos_cc_var_mad_outlier_featselect_sphering_harmony"),
    ("COMPOUND", "profiles_var_mad_int_featselect_harmony"),
)

filepaths = {
    dset: f"{_PREFIX}/{_RECIPE}/{dset}/{transform}/profiles.parquet"
    for dset, transform in transforms
}

# %% [markdown] Define functions
# We use a S3FileSystem to avoid the need of credentials.

# %%
def lazy_load(path: str) -> pl.LazyFrame:
    fs = S3FileSystem(anon=True)
    myds = dataset(path, filesystem=fs)
    df = pl.scan_pyarrow_dataset(myds)
    return df


# %% [markdown]
# We will lazy-load the dataframes and print the number of rows and columns

# %%
info = {k: [] for k in ("dataset", "#rows", "#cols", "#Metadata cols", "Size (MB)")}
for name, path in filepaths.items():
    data = lazy_load(path)
    n_rows = data.select(pl.count()).collect().item()
    metadata_cols = data.select(pl.col("^Metadata.*$")).columns
    n_cols = data.width
    n_meta_cols = len(metadata_cols)
    estimated_size = int(round(4.03 * n_rows * n_cols / 1e6, 0))  # B -> MB
    for k, v in zip(info.keys(), (name, n_rows, n_cols, n_meta_cols, estimated_size)):
        info[k].append(v)

pl.DataFrame(info)

# %% [markdown]
# Let us now focus on the crispr dataset and use a regex to select the metadata columns.
# We will then sample rows and display the overview.
# Note that the collect() method enforces loading some data into memory.

# %%
data = lazy_load(filepaths["CRISPR"])
data.select(pl.col("^Metadata.*$").sample(n=5, seed=1)).collect()

# %% [markdown]
# The following line excludes the metadata columns:

# %%
data_only = data.select(pl.all().exclude("^Metadata.*$").sample(n=5, seed=1)).collect()
data_only

# %% [markdown]
# Finally, we can convert this to pandas if we want to perform analyses with that tool.
# Keep in mind that this loads the entire dataframe into memory.

# %%
data_only.to_pandas()
