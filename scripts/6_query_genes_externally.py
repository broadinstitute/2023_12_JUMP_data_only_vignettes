#!/usr/bin/env jupyter
# ---
# title: Query information of genes
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
# This how-to focuses on linking gene names outside. Whilst not JUMP-specific, it is useful to fetch more information on perturbations that our analysis deem important without having to manually search them. We will use [Biopython](https://biopython.org/), this only explores a subset of the options, the full Entrez [documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/), which contains all the options, is a useful reference to keep in hand..
# %% Imports
import polars as pl
from Bio import Entrez
from broad_babel.query import get_mapper

# %% [markdown]
# We define
# %%

Entrez.email = "example@email.com"
fields = (
    "Name",
    "Description",
    "Summary",
    "OtherDesignations",  # This gives us synonyms
)
# %% [markdown]
# We will use a set of genes that we found in a JUMP cluster as an example.
# %%
genes = ("CHRM4", "SCAPER", "GPR176", "LY6K")
# %% [markdown]
# Get the
# %%
# Get a dictionary that maps Gene symbols to Entrez IDs
ids = get_mapper(
    query=genes,
    input_column="standard_key",
    output_columns="standard_key,NCBI_Gene_ID",
)

# Fetch the summaries for these genes
entries = []
for id_ in ids.values():
    stream = Entrez.esummary(db="gene", id=id_)
    record = Entrez.read(stream)

    entries.append(
        {k: record["DocumentSummarySet"]["DocumentSummary"][0][k] for k in fields}
    )

# %% Show the columns in a nice way
pl.DataFrame(entries)
