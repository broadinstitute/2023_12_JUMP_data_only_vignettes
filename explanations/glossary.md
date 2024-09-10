- [Definitions](#Definitions)
  - [Cytomining](#Cytomining)
- [Acronyms](#Acronyms)

Reference for terms and their definition.


<a id="Definitions"></a>

# Definitions

-   Morphological profiling: Method to study cell phenotypes by quantifying their shape, size and intensity features.
-   Phenotypic activity: Metric that indicates how well can we distinguish a perturbation from its negative controls.
-   Phenotypic consistency: Metric that indicates how well does a perturbation match an annotated resource (e.g., gene-target known interactions) (TODO add ref).
-   Phenotypic distinctiveness: Metric showing how distinctive a perturbation is relative to the other perturbations in a given experiment (TODO add ref).
-   Cosine similarity: Metric correlated to how close two vectors are. It assumes all the elements in them (usually features) have the same weight.
-   Retrievability: Umbrella term for the methods that assess the quality of a set of samples in a profiling experiment: phenotypic activity, consistency and distinctiveness.
-   Consensus profile: Aggregated profiles across all biological replicates (e.g., across all wells) of a given perturbation, generally it is the median of every feature.


<a id="Cytomining"></a>

## Cytomining

These definitions are related to [cytomining](https://github.com/cytomining) libraries and may not be relevant to the more recent tools. They are kept for future reference.

external\_metadata: Additional information for compounds, the essential metadata are (Plate\_Map\_Name, well\_position and broad\_sample). poscon\_diverse: Other positive controls, this is experiment-specific. poscon\_cp: Standard positive control used for compound studies(cp stands for compound probes). q-value: Expected False Discovery Rate (FDR): the proportion of false positives among all positive results. Replicate profile: Aggregation of single-cell profiles (e.g., across all cells in a single well), usually the median of all cells in a field of view.


<a id="Acronyms"></a>

# Acronyms

-   JUMP: Joint Undertaking for Morphological Profiling
-   mAP: mean Average Precision
-   CRISPR: Clustered Regularly Interspaced Short Palindromic Repeats. This method was used to produce the CRISPR datasets, whence genes were knocked-out.
-   ORF: Open Reading Frame. The ORF dataframe is comprised of overexpressed genes.
