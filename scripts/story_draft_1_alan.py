"""

Explore JUMP story specified on https://github.com/broadinstitute/2023_12_JUMP_data_only_vignettes/issues/15 
"""
import polars as pl
from utils import genes_to_summaries

clusters = {
    "A": ["LZTS2", "MYT1"],
    "B": ["CHRM4", "SLC22A14", "SCAPER", "TSC22D1", "GPR176", "LY6K"],
}
df = genes_to_summaries(tuple(y for x in clusters.values() for y in x))
with pl.Config(fmt_str_lengths=1000, set_tbl_width_chars=90):
    print(df)
# %% [markdown]
"""
## First impressions
Though generally unrelated, we can make small subgroups with genes that share a similar function.
### Group 1
- MYT1 CHRM4 and GPR176 (https://pubmed.ncbi.nlm.nih.gov/7893747/) are all involved in processes related to the nervous system. MYT1 anticorrelates strongly with CHRM4.
- CHRM4 correlates strongly (>0.7) with GPT176. Despite this, GPR176 and MYT1 only present a ~0.25 correlation.

### Group 2
- TSC22D1 and LZTS2 have a ~.37 correlation value. They both belong to the Leucine Zipper family and in tumor supression. LZTS2 is negatively correlated and it happens to be a negative correlation too.
#
"""
