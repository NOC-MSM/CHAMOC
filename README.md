# CHAMOC
Code and data to recreate the results of the paper:

Agathe Germe, Joel J.-M. Hirschi, Adam T. Blaker and Bablu Sinha (2022) Chaotic variability of the Atlantic meridional overturning circulation at sub-annual time scales, JPO

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5911238.svg)](https://doi.org/10.5281/zenodo.5911238)

## Quick Start:

```
git clone git@github.com:NOC-MSM/CHAMOC.git
```
or
```
git clone https://github.com/NOC-MSM/PyNEMO.git
```

## Create python environment
```
{conda,mamba} env create --file environment.yml
conda activate CHAMOC
```

```
PYTHONPATH="${PYTHONPATH}:${PWD}/src/TOOLS/PYTHON/mymodules"
export PYTHONPATH
```


## To run the R scripts

```
module load jasr/3.6/r20211105

Rscript figure_07.R
Rscript figure_09.R
```
