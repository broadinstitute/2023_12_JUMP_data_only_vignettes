## Quirks and details

There are additional details that are not commonly asked but it is important to retain on record. This is a compendium of those.

- Source 2 and 9 use larger plates (1536 vs the standard 384\)  
- Source 7 and 13 are the same  
- In JUMP-Target there is an InChIKey that maps to 2 different perturbations: ‘LOUPRKONTZGTKE-UHFFFAOYSA-N’ maps to both quinidine and quinine.  
- The definition of controls, specially positive controls, can be tricky: Some are hard-coded in [broad\_babel](https://github.com/broadinstitute/monorepo/blob/febe56c27e490c110d8b5a871de974a4293176c6/libs/jump_babel/tools/gen_database.py#L70-L87), based on internal knowledge that was not recorded at the time of assembling the datasets. In certain datasets, such as ORF, there are additional types of positive controls: poscon\_orf, poscon\_cp (compound probe), and poscon\_diverse.