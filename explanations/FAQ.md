- [Frequently Asked Questions](#Frequently-Asked-Questions)
  - [Analyses](#Analyses)
    - [How can I reproduce an environment to explore JUMP data?](#How-can-I-reproduce-an-environment-to-explore-JUMP-data)
  - [Data](#Data)
    - [Does JUMP contain X compound/gene?](#Does-JUMP-contain-X-compound-gene)
    - [Where are the datasets specification?](#Where-are-the-datasets-specification)
    - [Why are some images with corresponding images but no downstream analysis?](#Why-are-some-images-with-corresponding-images-but-no-downstream-analysis)
    - [Why do some perturbations have so many replicates](#Why-do-some-perturbations-have-so-many-replicates)
    - [How were the profiles created?](#How-were-the-profiles-created)
    - [Do we we expect one JCP to have multiple targets?](#Do-we-we-expect-one-JCP-to-have-multiple-targets)
    - [Do JCPs within either the CRISPR or ORF share the same gene?](#Do-JCPs-within-either-the-CRISPR-or-ORF-share-the-same-gene)
    - [Web interfaces](#Web-interfaces)

Frequently Asked Questions and links to their answers. They are grouped based on whether they pertain to data, libraries or analyses.


<a id="Frequently-Asked-Questions"></a>

# Frequently Asked Questions


<a id="Analyses"></a>

## Analyses


<a id="How-can-I-reproduce-an-environment-to-explore-JUMP-data"></a>

### How can I reproduce an environment to explore JUMP data?

(WIP) The easiest way to set things up will be installing from pip in your enviromnment of choice:

```bash
pip install jump-pills
```


<a id="Data"></a>

## Data


<a id="Does-JUMP-contain-X-compound-gene"></a>

### Does JUMP contain X compound/gene?

The easiest way to find out is querying your dataset using [this](https://broad.io/babel) web tool. Alternatively, you can explore the [metadata tables](https://github.com/jump-cellpainting/datasets/tree/main/metadata) on the datasets repository.


<a id="Where-are-the-datasets-specification"></a>

### Where are the datasets specification?

The main resource to understand the technicalities of the JUMP datasets collection and assembly is on this [repo](https://github.com/jump-cellpainting/datasets).


<a id="Why-are-some-images-with-corresponding-images-but-no-downstream-analysis"></a>

### Why are some images with corresponding images but no downstream analysis?

Some plates failed Quality Control (QC) but we kept them because they may be useful for developing QC methods.


<a id="Why-do-some-perturbations-have-so-many-replicates"></a>

### Why do some perturbations have so many replicates

Most plates contain 16 negative control wells, while some have as many as 28 wells. One replicate of four of the compound positive controls are added to wells O23, O24, P23 and P24. The remaining wells contain ORF treatments, with a single replicate of each per plate map and with five replicate plates produced per plate map ([issue](https://github.com/jump-cellpainting/megamap/issues/8#issuecomment-1413606031)).


<a id="How-were-the-profiles-created"></a>

### How were the profiles created?

We used snakemake and pycytominer to generate these. The details can be found in [this](https://github.com/broadinstitute/jump-profiling-recipe) repo.


<a id="Do-we-we-expect-one-JCP-to-have-multiple-targets"></a>

### Do we we expect one JCP to have multiple targets?

Yes, there will be many with multiple targets. For instance, `JCP2022_050797` (quinidine/quinine) has the targets `KCNK1` and `KCNN4`.

Two were considered to be two different compounds because they had different names and `broad_sample` names. But after all the data cleanup steps, they ended up being the same. Hence two different entries.


<a id="Do-JCPs-within-either-the-CRISPR-or-ORF-share-the-same-gene"></a>

### Do JCPs within either the CRISPR or ORF share the same gene?

In CRISPR each JCP ID corresponds to a different gene. But in ORF there are sometimes multiple reagents targeting the same gene. In this case, we compute consensus profiles at the gene level (more info [here](https://github.com/jump-cellpainting/morphmap/issues/178)).


<a id="Web-interfaces"></a>

### Web interfaces

1.  What is the source of the replicability metric?

    These two files ([ORF](https://github.com/jump-cellpainting/2024_Chandrasekaran_Morphmap/blob/c47ad6c953d70eb9e6c9b671c5fe6b2c82600cfc/03.retrieve-annotations/output/phenotypic-activity-wellpos_cc_var_mad_outlier_featselect_sphering_harmony.csv.gz) and [CRISPR](https://github.com/jump-cellpainting/2024_Chandrasekaran_Morphmap/blob/c47ad6c953d70eb9e6c9b671c5fe6b2c82600cfc/03.retrieve-annotations/output/phenotypic-activity-wellpos_cc_var_mad_outlier_featselect_sphering_harmony_PCA_corrected.csv.gz)) contain the mAP and corrected p values for replicate retrieval. They won't contain all ORF and CRISPR reagents because so of them were filtered out for qc reasons.

2.  X\_Feature: For each row, is the `Feature` value an average for all the cells in the `Metadata_image` using the listed `Mask`? Or is it associated with a single cell in that image?

    Any `Feature` is the average of all cells and all replicates (typically four in total) for the specific mask and feature.

3.  How are `Statistic` and `Median` calculated for each row? Are they calculated in relation to the average of the "Feature" values for the negative controls in the same plate?

    -   `Statistic` is the probability of a given distribution (four replicates) to occur relative to their negative controls (in the four plates, typically each replicate is in an independent plate).
    -   `Median` is the median feature across all (~4) replicates. Each of these replicates' value was in turn the mean of all the sites and cells in a given well.
