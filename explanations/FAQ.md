- [Analyses](#Analyses)
  - [How can I reproduce an environment to explore JUMP data?](#How%20can%20I%20reproduce%20an%20environment%20to%20explore%20JUMP%20data%3F)
- [Data](#Data)
  - [Where are the datasets specification?](#Where%20are%20the%20datasets%20specification%3F)
  - [Why are some images with corresponding images but no downstream analysis?](#Why%20are%20some%20images%20with%20corresponding%20images%20but%20no%20downstream%20analysis%3F)
  - [Why do some perturbations have so many replicates](#Why%20do%20some%20perturbations%20have%20so%20many%20replicates)

Frequently Asqued Questions and links to their answers. They are grouped based on whether they pertain to data, libraries or analyses.


<a id="Analyses"></a>

# Analyses


<a id="How%20can%20I%20reproduce%20an%20environment%20to%20explore%20JUMP%20data%3F"></a>

## How can I reproduce an environment to explore JUMP data?

(WIP) The easiest way to set things up will be installing from pip in your enviromnment of choice:

```bash
pip install jump-pills
```


<a id="Data"></a>

# Data


<a id="Where%20are%20the%20datasets%20specification%3F"></a>

## Where are the datasets specification?

The main resource to understand the technicalities of the JUMP datasets collection and assembly is on this [repo](https://github.com/jump-cellpainting/datasets).


<a id="Why%20are%20some%20images%20with%20corresponding%20images%20but%20no%20downstream%20analysis%3F"></a>

## Why are some images with corresponding images but no downstream analysis?

Some plates failed Quality Control (QC) but we kept them because they may be useful for developing QC methods.


<a id="Why%20do%20some%20perturbations%20have%20so%20many%20replicates"></a>

## Why do some perturbations have so many replicates

temp Most plates contain 16 negative control wells, while some have as many as 28 wells. One replicate of four of the compound positive controls are added to wells O23, O24, P23 and P24. The remaining wells contain ORF treatments, with a single replicate of each per plate map and with five replicate plates produced per plate map^[ref](https://github.com/jump-cellpainting/megamap/issues/8#issuecomment-1413606031).
