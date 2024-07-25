# jupyter:
#  jupytext:
#    cell_markers:  '"""'
"""
Explore JUMP story specified on https://github.com/broadinstitute/2023_12_JUMP_data_only_vignettes/issues/15 
"""
import polars as pl
from utils import genes_to_summaries

clusters = {
    "A": ["LZTS2", "MYT1"],
    "B": ["CHRM4", "SLC22A14", "SCAPER", "TSC22D1", "GPR176", "LY6K"],
}
symbols = tuple(y for x in clusters.values() for y in x)
df = genes_to_summaries(symbols)
df = genes_to_summaries(symbols).sort(pl.col("Name").cast(pl.Enum(symbols)))
with pl.Config(fmt_str_lengths=1000, set_tbl_width_chars=70):
    print(df.select(pl.col(["Name", "Summary"])))
    # %% [markdown]
    """
┌──────────┬───────────────────────────────────────────────────────────────────┐
│ Name     ┆ Summary                                                           │
│ ---      ┆ ---                                                               │
│ str      ┆ str                                                               │
╞══════════╪═══════════════════════════════════════════════════════════════════╡
│ LZTS2    ┆ The protein encoded by this gene belongs to the leucine zipper    │
│          ┆ tumor suppressor family of proteins, which function in            │
│          ┆ transcription regulation and cell cycle control. This family      │
│          ┆ member can repress beta-catenin-mediated transcriptional          │
│          ┆ activation and is a negative regulator of the Wnt signaling       │
│          ┆ pathway. It negatively regulates microtubule severing at          │
│          ┆ centrosomes, and is necessary for central spindle formation and   │
│          ┆ cytokinesis completion. It is implicated in cancer, where it may  │
│          ┆ inhibit cell proliferation and decrease susceptibility to tumor   │
│          ┆ development. Alternative splicing of this gene results in         │
│          ┆ multiple transcript variants. [provided by RefSeq, Dec 2015]      │
│ MYT1     ┆ The protein encoded by this gene is a member of a family of       │
│          ┆ neural specific, zinc finger-containing DNA-binding proteins. The │
│          ┆ protein binds to the promoter regions of proteolipid proteins of  │
│          ┆ the central nervous system and plays a role in the developing     │
│          ┆ nervous system. [provided by RefSeq, Jul 2008]                    │
│ CHRM4    ┆ The muscarinic cholinergic receptors belong to a larger family of │
│          ┆ G protein-coupled receptors. The functional diversity of these    │
│          ┆ receptors is defined by the binding of acetylcholine and includes │
│          ┆ cellular responses such as adenylate cyclase inhibition,          │
│          ┆ phosphoinositide degeneration, and potassium channel mediation.   │
│          ┆ Muscarinic receptors influence many effects of acetylcholine in   │
│          ┆ the central and peripheral nervous system. The clinical           │
│          ┆ implications of this receptor are unknown; however, mouse studies │
│          ┆ link its function to adenylyl cyclase inhibition. [provided by    │
│          ┆ RefSeq, Jul 2008]                                                 │
│ SLC22A14 ┆ This gene encodes a member of the organic-cation transporter      │
│          ┆ family. It is located in a gene cluster with another member of    │
│          ┆ the family, organic cation transporter like 3. The encoded        │
│          ┆ protein is a transmembrane protein which is thought to transport  │
│          ┆ small molecules and since this protein is conserved among several │
│          ┆ species, it is suggested to have a fundamental role in mammalian  │
│          ┆ systems. Alternative splicing results in multiple transcript      │
│          ┆ variants. [provided by RefSeq, Feb 2016]                          │
│ SCAPER   ┆ Predicted to enable nucleic acid binding activity and zinc ion    │
│          ┆ binding activity. Located in cytosol and nuclear speck. [provided │
│          ┆ by Alliance of Genome Resources, Apr 2022]                        │
│ TSC22D1  ┆ This gene encodes a member of the TSC22 domain family of leucine  │
│          ┆ zipper transcription factors. The encoded protein is stimulated   │
│          ┆ by transforming growth factor beta, and regulates the             │
│          ┆ transcription of multiple genes including C-type natriuretic      │
│          ┆ peptide. The encoded protein may play a critical role in tumor    │
│          ┆ suppression through the induction of cancer cell apoptosis, and a │
│          ┆ single nucleotide polymorphism in the promoter of this gene has   │
│          ┆ been associated with diabetic nephropathy. Alternatively spliced  │
│          ┆ transcript variants encoding multiple isoforms have been observed │
│          ┆ for this gene. [provided by RefSeq, Aug 2011]                     │
│ GPR176   ┆ Members of the G protein-coupled receptor family, such as GPR176, │
│          ┆ are cell surface receptors involved in responses to hormones,     │
│          ┆ growth factors, and neurotransmitters (Hata et al., 1995 [PubMed  │
│          ┆ 7893747]).[supplied by OMIM, Jul 2008]                            │
│ LY6K     ┆ Predicted to be involved in binding activity of sperm to zona     │
│          ┆ pellucida. Predicted to act upstream of or within flagellated     │
│          ┆ sperm motility. Predicted to be located in cell surface;          │
│          ┆ cytoplasm; and plasma membrane. Predicted to be active in         │
│          ┆ acrosomal vesicle. [provided by Alliance of Genome Resources, Apr │
│          ┆ 2022]                                                             │
└──────────┴───────────────────────────────────────────────────────────────────┘
## First impressions
Though generally unrelated, we can make small subgroups with genes that share a similar function.
### Group 1
- MYT1 CHRM4 and GPR176 (https://pubmed.ncbi.nlm.nih.gov/7893747/) are all involved in processes related to the nervous system. MYT1 anticorrelates strongly with CHRM4.
- CHRM4 correlates strongly (>0.7) with GPT176. Despite this, GPR176 and MYT1 only present a ~0.25 correlation.

### Group 2
- TSC22D1 and LZTS2 have a ~.37 correlation value. They both belong to the Leucine Zipper family and in tumor supression. LZTS2 is a negative regulator of Wnt signaling pathway, while also being negatively correlated to TSC22D1.
#
"""
    # %%
    from Bio import Entrez
    from broad_babel.query import get_mapper

    mapper = get_mapper(
        symbols, input_column="standard_key", output_columns="standard_key,NCBI_Gene_ID"
    )
