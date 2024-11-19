# Getting Started with JUMP

What is the purpose of this website? To provide up-to-date info on everything JUMP-related. We aim to minimize friction for developers, technical writers and biologists to produce and access novel insights and tools. We aim to make this the one-stop shop for the vast majority of JUMP questions, be it computational or biological.

## Choose Your Own Path

1. **Just exploring the data?**  
     
   - Use a web interface; no programming required:  
     * [JUMP-CP Data Explorer](https://phenaid.ardigen.com/jumpcpexplorer/) by Ardigen,   
     * [JUMP-CP Data Portal](https://www.springscience.com/jump-cp) by Spring Discovery,   
     * [JUMPer tools](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_rr#quick-data-access) by Carpenter–Singh Lab (Muñoz et al.)   
     * Morpheus by Broad Institute

   You can look up images for a sample, distinguishing features, most-similar genes or compounds, and more\!

   

2. **Want to fetch and analyze data?**  
     
   - Follow our [how-to guides](http://howto/) for common analyses

   

3. **Looking to build tools?**  
     
   - Use our Python libraries [cpgdata](https://github.com/broadinstitute/cpg/tree/main/cpgdata), [jump-portrait](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_portrait), [jump-babel](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_babel) and other libraries in the [monorepo](https://github.com/broadinstitute/monorepo/tree/main)  
   - Access the [metadata schema](https://github.com/jump-cellpainting/datasets/tree/main/metadata)

## Need help or more information?

- Read the papers creating the datasets for experimental and analysis details:  
  - [CPJUMP1](https://www.nature.com/articles/s41592-024-02241-6)  
  - JUMP data prod biorxiv  
  - Morphmap biorxiv  
- Raise an issue or ask a question on [Github](https://github.com/jump-cellpainting/datasets/issues)  
- Subscribe to updates at [jump-cellpainting.broadinstitute.org/more-info](https://jump-cellpainting.broadinstitute.org/more-info)


### How can I access the How-To guides in a live coding environment?

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

