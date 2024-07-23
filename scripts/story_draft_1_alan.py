"""

Explore JUMP story specified on https://github.com/broadinstitute/2023_12_JUMP_data_only_vignettes/issues/15 
"""
import polars as pl
from Bio import Entrez
from broad_babel.query import get_mapper

Entrez.email = "amunozgo@broadinstitute.org"
# %%

clusters = {
    "A": ["LZTS2", "MYT1"],
    "B": ["CHRM4", "SLC22A14", "SCAPER", "TSC22D1", "GPR176", "LY6K"],
}


# %% Convert to entrez ids using broad_babel
ids = get_mapper(
    query=tuple(val for vals in clusters.values() for val in vals),
    input_column="standard_key",
    output_columns="standard_key,NCBI_Gene_ID",
)

# %% Fetch summaries
entries = []
fields = (
    "Name",
    "Description",
    "Summary",
    # "OtherDesignations",
)
for id_ in ids.values():
    print(id_)
    stream = Entrez.esummary(db="gene", id=id_)
    record = Entrez.read(stream)

    entries.append(
        {k: record["DocumentSummarySet"]["DocumentSummary"][0][k] for k in fields}
    )

# %% Show the columns in a nice way
df = pl.DataFrame(entries)
with pl.Config(fmt_str_lengths=1000, set_tbl_width_chars=120):
    print(df)

# %% [markdown]
# ## First impressions
# - MYT1 CHRM4 and GPR176 are all involved in processes related to the nervous system. MYT1 anticorrelates strongly with CHRM4. CHRM4 correlates strongly (>0.7) with GPT176. Despite this, GPR176 and MYT1 only present a ~0.25 correlation.
# - TSC22D1 and LZTS2 have a ~.37 correlation value. They both belong to the Leucine Zipper family and in tumor supression. LZTS2 is negatively correlated and it happens to be a negative correlation too.

# -
