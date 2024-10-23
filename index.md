# Overview

The purpose of this resource is to concentrate all the useful and up-to-date information necessary to make use of [JUMP](https://jump-cellpainting.broadinstitute.org/). JUMP stands for Joint Undertaking for Morphological Profiling, and the JUMP-Cell Painting Consortium it is a collaboration between multiple academic and industrial partners to produce the largest [Cell Painting](https://jump-cellpainting.broadinstitute.org/cell-painting) dataset comprised of images and morphological profiles of genetically or chemically perturbed cells. This website aims to summarise the most useful information, including examples, guides, know-hows and links to more material for deeper dives into data acquisition, processing, sharing and visualization.

## I just want to access the web tools

[Here](https://github.com/broadinstitute/monorepo/blob/main/libs/jump_rr/README.md#Quick%20data%20access) you can find the up-to-date web tools to explore JUMP from your browser. These are very useful for querying perturbations without needing experience in data analysis or programming. They are also very convenient for a one-off query of the dataset.


## I am a developer interested in using and writing programatic tools for JUMP

Our [monorepo](https://github.com/broadinstitute/monorepo/tree/main) hosts Python libraries that may help you access JUMP data in a high-throughput manner.


## How can I access the How-To guides in a live coding environment?

This table provides direct link to run the guides on your browser. Google Colab is the only supported live-coding web interface.

| Google Collab                                                                                                                                                                |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Retrieve JUMP profiles](https://colab.research.google.com/github/broadinstitute/2023_12_JUMP_data_only_vignettes/blob/colab/colab/1_retrieve_profiles.ipynb)                   |
| [Add metadata to profiles](https://colab.research.google.com/github/broadinstitute/2023_12_JUMP_data_only_vignettes/blob/colab/colab/2_add_metadata.ipynb)                   |
| [Calculate phenotypic activity](https://colab.research.google.com/github/broadinstitute/2023_12_JUMP_data_only_vignettes/blob/colab/colab/3_calculate_activity.ipynb)        |
| [Display perturbation images](https://colab.research.google.com/github/broadinstitute/2023_12_JUMP_data_only_vignettes/blob/colab/colab/4_display_perturbation_images.ipynb) |
| [Explore perturbation clusters](https://colab.research.google.com/github/broadinstitute/2023_12_JUMP_data_only_vignettes/blob/colab/colab/5_explore_distance_clusters.ipynb) |
| [Query genes for more info](https://colab.research.google.com/github/broadinstitute/2023_12_JUMP_data_only_vignettes/blob/colab/colab/6_query_genes_externally.ipynb)        |

Alternatively, you can download the notebooks from their respective pages and run them in your local Python environment. We have published a package containing all dependencies, you need only install in your environment using `pip install jump_deps` (Python 3.10 or 3.11).


## What is the purpose of this website?

To provide up-to-date info on everything JUMP-related. We aim to minimize friction for developers, technical writers and biologists to produce and access novel insights and tools. We believe complexity is one of the biggest challenges in challenge, hampering collaboration and novel biological insights. We aim to make this the one-stop shop for the vast majority of JUMP questions, be it computational or biological.
