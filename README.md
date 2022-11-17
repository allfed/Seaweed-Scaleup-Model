# Seaweed Scale-Up Model   

---


[![DOI](https://zenodo.org/badge/520046482.svg)](https://zenodo.org/badge/latestdoi/520046482)
![Testing](https://github.com/allfed/seaweed-upscaling-model/actions/workflows/testing.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


---


## Installation
We recommend setting up a virtual environment to install this model and all its dependencies. A more in depth explanation of virtual environments can be found [here](https://goodresearch.dev/). The short version is: just create a virtual environment from the `environment.yml` file here by using either conda or mamba:

`conda env create -f environment.yml`

This will create a virtual environment called "seaweed-scaleup-model". Once you activated it, you can install this model as a package into it by running the following line in the main folder of the repository:

`pip install -e .`

When you follow these steps you should have a virtual environment that is able to run the seaweed growth model. If you run into any problems feel free to open an issue in this repository or contact IT-support@allfed.info. 

## How this model works in general

![Model](https://raw.githubusercontent.com/allfed/Seaweed-Growth-Model/main/results/model_description/structure.png)

This model takes the output of the [seaweed growth model](https://github.com/allfed/Seaweed-Growth-Model) and simulates the scale-up of seaweed production in nuclear winter. To do so it creates a fixed amount of new seaweed farms each day it runs. If the seaweed on the existing farms has reached the threshold density, it is harvested. Once it is harvested, the yield is used to stock newly build areas with seaweed. If there are no areas to be stocked up the yield is used for consumption. 

## Structure

The code in this repository is split into three parts:

### The actual model

The model can be found in `scaleup_model.py`. It has a variety of variables that can be changed to simulate different scenarios. For example, the duration of the simulation, the threshold density for harvest or how much of the yield is lost to waste.

### Preprocessing

The preprocessing reformats the data from the seaweed growth model and saves it in this new format. 

### Plotting

Makes the plots for the publication. 




