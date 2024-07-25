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
"""
─────────┬───────────────────────────────────────┬──────────────────────────────────────┐
│ Name    ┆ Description                           ┆ Summary                              │
│ ---     ┆ ---                                   ┆ ---                                  │
│ str     ┆ str                                   ┆ str                                  │
╞═════════╪═══════════════════════════════════════╪══════════════════════════════════════╡
│ PVR     ┆ PVR cell adhesion molecule            ┆ The protein encoded by this gene is  │
│         ┆                                       ┆ a transmembrane glycoprotein         │
│         ┆                                       ┆ belonging to the immunoglobulin      │
│         ┆                                       ┆ superfamily. The external domain     │
│         ┆                                       ┆ mediates cell attachment to the      │
│         ┆                                       ┆ extracellular matrix molecule        │
│         ┆                                       ┆ vitronectin, while its intracellular │
│         ┆                                       ┆ domain interacts with the dynein     │
│         ┆                                       ┆ light chain Tctex-1/DYNLT1. The gene │
│         ┆                                       ┆ is specific to the primate lineage,  │
│         ┆                                       ┆ and serves as a cellular receptor    │
│         ┆                                       ┆ for poliovirus in the first step of  │
│         ┆                                       ┆ poliovirus replication. Multiple     │
│         ┆                                       ┆ transcript variants encoding         │
│         ┆                                       ┆ different isoforms have been found   │
│         ┆                                       ┆ for this gene. [provided by RefSeq,  │
│         ┆                                       ┆ Oct 2008]                            │
│ UQCRFS1 ┆ ubiquinol-cytochrome c reductase,     ┆ Predicted to enable oxidoreductase   │
│         ┆ Rieske iron-sulfur polypeptide 1      ┆ activity. Involved in mitochondrial  │
│         ┆                                       ┆ respiratory chain complex III        │
│         ┆                                       ┆ assembly and respiratory electron    │
│         ┆                                       ┆ transport chain. Located in          │
│         ┆                                       ┆ mitochondrion. Part of mitochondrial │
│         ┆                                       ┆ respiratory chain complex III and    │
│         ┆                                       ┆ mitochondrial respiratory chain      │
│         ┆                                       ┆ complex IV. Implicated in            │
│         ┆                                       ┆ mitochondrial complex III            │
│         ┆                                       ┆ deficiency. [provided by Alliance of │
│         ┆                                       ┆ Genome Resources, Apr 2022]          │
│ ECH1    ┆ enoyl-CoA hydratase 1                 ┆ This gene encodes a member of the    │
│         ┆                                       ┆ hydratase/isomerase superfamily. The │
│         ┆                                       ┆ gene product shows high sequence     │
│         ┆                                       ┆ similarity to enoyl-coenzyme A (CoA) │
│         ┆                                       ┆ hydratases of several species,       │
│         ┆                                       ┆ particularly within a conserved      │
│         ┆                                       ┆ domain characteristic of these       │
│         ┆                                       ┆ proteins. The encoded protein, which │
│         ┆                                       ┆ contains a C-terminal peroxisomal    │
│         ┆                                       ┆ targeting sequence, localizes to the │
│         ┆                                       ┆ peroxisome. The rat ortholog, which  │
│         ┆                                       ┆ localizes to the matrix of both the  │
│         ┆                                       ┆ peroxisome and mitochondria, can     │
│         ┆                                       ┆ isomerize 3-trans,5-cis-dienoyl-CoA  │
│         ┆                                       ┆ to 2-trans,4-trans-dienoyl-CoA,      │
│         ┆                                       ┆ indicating that it is a              │
│         ┆                                       ┆ delta3,5-delta2,4-dienoyl-CoA        │
│         ┆                                       ┆ isomerase. This enzyme functions in  │
│         ┆                                       ┆ the auxiliary step of the fatty acid │
│         ┆                                       ┆ beta-oxidation pathway. Expression   │
│         ┆                                       ┆ of the rat gene is induced by        │
│         ┆                                       ┆ peroxisome proliferators. [provided  │
│         ┆                                       ┆ by RefSeq, Jul 2008]                 │
│ SARS2   ┆ seryl-tRNA synthetase 2,              ┆ This gene encodes the mitochondrial  │
│         ┆ mitochondrial                         ┆ seryl-tRNA synthethase precursor, a  │
│         ┆                                       ┆ member of the class II tRNA          │
│         ┆                                       ┆ synthetase family. The mature enzyme │
│         ┆                                       ┆ catalyzes the ligation of Serine to  │
│         ┆                                       ┆ tRNA(Ser) and participates in the    │
│         ┆                                       ┆ biosynthesis of                      │
│         ┆                                       ┆ selenocysteinyl-tRNA(sec) in         │
│         ┆                                       ┆ mitochondria. The enzyme contains an │
│         ┆                                       ┆ N-terminal tRNA binding domain and a │
│         ┆                                       ┆ core catalytic domain. It functions  │
│         ┆                                       ┆ in a homodimeric form, which is      │
│         ┆                                       ┆ stabilized by tRNA binding. This     │
│         ┆                                       ┆ gene is regulated by a bidirectional │
│         ┆                                       ┆ promoter that also controls the      │
│         ┆                                       ┆ expression of mitochondrial          │
│         ┆                                       ┆ ribosomal protein S12. Both genes    │
│         ┆                                       ┆ are within the critical interval for │
│         ┆                                       ┆ the autosomal dominant deafness      │
│         ┆                                       ┆ locus DFNA4 and might be linked to   │
│         ┆                                       ┆ this disease. Multiple transcript    │
│         ┆                                       ┆ variants encoding different isoforms │
│         ┆                                       ┆ have been identified for this gene.  │
│         ┆                                       ┆ [provided by RefSeq, Mar 2009]       │
│ LAIR1   ┆ leukocyte associated immunoglobulin   ┆ The protein encoded by this gene is  │
│         ┆ like receptor 1                       ┆ an inhibitory receptor found on      │
│         ┆                                       ┆ peripheral mononuclear cells,        │
│         ┆                                       ┆ including natural killer cells, T    │
│         ┆                                       ┆ cells, and B cells. Inhibitory       │
│         ┆                                       ┆ receptors regulate the immune        │
│         ┆                                       ┆ response to prevent lysis of cells   │
│         ┆                                       ┆ recognized as self. The gene is a    │
│         ┆                                       ┆ member of both the immunoglobulin    │
│         ┆                                       ┆ superfamily and the                  │
│         ┆                                       ┆ leukocyte-associated inhibitory      │
│         ┆                                       ┆ receptor family. The gene maps to a  │
│         ┆                                       ┆ region of 19q13.4 called the         │
│         ┆                                       ┆ leukocyte receptor cluster, which    │
│         ┆                                       ┆ contains at least 29 genes encoding  │
│         ┆                                       ┆ leukocyte-expressed receptors of the │
│         ┆                                       ┆ immunoglobulin superfamily. The      │
│         ┆                                       ┆ encoded protein has been identified  │
│         ┆                                       ┆ as an anchor for tyrosine            │
│         ┆                                       ┆ phosphatase SHP-1, and may induce    │
│         ┆                                       ┆ cell death in myeloid leukemias.     │
│         ┆                                       ┆ Alternative splicing results in      │
│         ┆                                       ┆ multiple transcript variants.        │
│         ┆                                       ┆ [provided by RefSeq, Jan 2014]       │
│ SLC1A5  ┆ solute carrier family 1 member 5      ┆ The SLC1A5 gene encodes a            │
│         ┆                                       ┆ sodium-dependent neutral amino acid  │
│         ┆                                       ┆ transporter that can act as a        │
│         ┆                                       ┆ receptor for RD114/type D retrovirus │
│         ┆                                       ┆ (Larriba et al., 2001 [PubMed        │
│         ┆                                       ┆ 11781704]).[supplied by OMIM, Jan    │
│         ┆                                       ┆ 2011]                                │
└─────────┴───────────────────────────────────────┴──────────────────────────────────────┘
"""
