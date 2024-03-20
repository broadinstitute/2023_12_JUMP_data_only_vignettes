#!/usr/bin/env jupyter
# ---
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

# %% Overview [markdown]
# # Basic JUMP data access
# This is a tutorial on how to access
# We will use polars to fetch the data frame lazily, with the help of s3fs and pyarrow.
# We prefer lazy loading because the data can be too big to be handled in memory.
# %% Imports
import polars as pl
from pyarrow.dataset import dataset
from s3fs import S3FileSystem

# %% [markdown]
# The shapes of the available datasets are:
# - crispr: Knock-out genetic perturbations.
# - orf: Overexpression genetic perturbations.
# - compounds: Chemical genetic perturbations.
#
# The aws paths of the dataframes are shown below:
# %% Paths
prefix = (
    "s3://cellpainting-gallery/cpg0016-jump-integrated/source_all/workspace/profiles"
)
filepaths = dict(
    crispr=f"{prefix}/chandrasekaran_2024_0000000/crispr/wellpos_cellcount_mad_outlier_nan_featselect_harmony.parquet",
    orf=f"{prefix}/chandrasekaran_2024_0000000/orf/wellpos_cellcount_mad_outlier_nan_featselect_harmony.parquet",
    compound=f"{prefix}/arevalo_2023_e834481/compound/mad_int_featselect_harmony.parquet/",
)


# %% [markdown]
# We use a S3FileSystem to avoid the need of credentials.
# %%
def lazy_load(path: str) -> pl.DataFrame:
    fs = S3FileSystem(anon=True)
    myds = dataset(path, filesystem=fs)
    df = pl.scan_pyarrow_dataset(myds)
    return df


# %% [markdown]
# We will lazy load the data to visualise its columns
# %%
print("Width, or number of columns.")
for name, path in filepaths.items():
    data = lazy_load(path)
    metadata_cols = [col for col in data.columns if col.startswith("Metadata")]
    print(f"{name}: {data.width}, containing {len(metadata_cols)} metadata columns")

# %% [markdown]
# Let us now focus on the crispr dataset and use a regex to select the metadata columns.
# Note that the collect() method enforces loading some data into memory.
# %%
data = lazy_load(filepaths["crispr"])
data.select(pl.col("^Metadata.*$").shuffle()).head().collect()
# %% [markdown]
# The previous block shows that the data frame has 51,850 rows.
# We can print features The regular expression used here to show the features present alongside the metadata.
# %%
header = data.select(pl.col("^X_harmony_000[0-4]$")).head().collect()
header
# %% [markdown]
# Finally, we can convert this to pandas if we want to analyse it using that way.
# Note that if we convert the entire dataframe to pandas it will load it all into memory.
# %%
header.to_pandas()
