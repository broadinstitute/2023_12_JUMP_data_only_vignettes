- [Glossary and Acronyms](#Glossary-and-Acronyms)
  - [Acronyms](#Acronyms)
- [Other definitions](#Other-definitions)

Reference for terms and their definition.


<a id="Glossary-and-Acronyms"></a>

# Glossary and Acronyms

-   **Morphological profiling** (aka image-based profiling): Method to study cell phenotypes by quantifying their shape, size and intensity features.
-   **Phenotypic activity**: Metric that indicates how well can we distinguish a perturbation from its negative controls [ref](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11014546/).
-   **Phenotypic consistency**: Metric that indicates how well does a perturbation match an annotated resource (e.g., gene-target known interactions).
-   **Phenotypic distinctiveness**: Metric showing how distinctive a perturbation is relative to the other perturbations in a given experiment.
-   **Cosine similarity**: Metric correlated to how close two vectors are. It assumes all the elements in them (usually features) have the same weight.
-   **Retrievability: Umbrella term for the methods that assess the quality of a set of samples in a profiling experiment**: phenotypic activity, consistency and distinctiveness.
-   **Consensus profile**: Aggregated profiles across all biological replicates (e.g., across all wells) of a given perturbation, generally it is the median of every feature.


<a id="Acronyms"></a>

## Acronyms

-   **JUMP**: Joint Undertaking for Morphological Profiling
-   **mAP**: mean Average Precision
-   **CRISPR**: Clustered Regularly Interspaced Short Palindromic Repeats. This method was used to produce the CRISPR datasets, whence genes were knocked-out.
-   **ORF**: Open Reading Frame. The ORF dataframe is comprised of overexpressed genes.


<a id="Other-definitions"></a>

# Other definitions

These definitions are related to [cytomining](https://github.com/cytomining) libraries and may not be relevant to the more recent tools. They are kept here in case you encounter them in papers/metadata.

-   **poscon\_diverse**: Other positive controls, this is experiment-specific.
-   **poscon\_cp**: Standard positive control used for compound studies(cp stands for compound probes).
-   **q-value: Expected False Discovery Rate (FDR)**: the proportion of false positives among all positive results.
