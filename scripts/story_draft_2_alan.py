"""

Explore JUMP story specified on https://github.com/broadinstitute/2023_12_JUMP_data_only_vignettes/issues/16 
"""
import polars as pl
from utils import genes_to_summaries

clusters = {
    "A": ["PVR", "UQCRFS1", "ECH1"],
    "B": ["SARS2", "LAIR1", "SLC1A5"],
}
symbols = tuple(y for x in clusters.values() for y in x)
df = genes_to_summaries(symbols).sort(pl.col("Name").cast(pl.Enum(symbols)))
df.with_columns(
    pl.col("Summary").str.extract("PubMed ([0-9]+)").alias("PubMed ID"),
    pl.col("Summary").str.replace("\[[ps].*\]$", ""),
)
with pl.Config(fmt_str_lengths=1000, set_tbl_width_chars=90):
    print(df.select(("Name", "Description", "Summary")))

for name, desc, summary, _, pubmed in df.iter_rows():
    pretty_str = f"{name}: {desc} {{}} \n {summary}"
    print(pretty_str.format(f"[Pubmed {pubmed}]" if pubmed else ""))
