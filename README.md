# CHAMOC
Code and data to recreate the results of the Germe et al. (2022) CHAMOC paper


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
