# Seaweed Scale-Up Model   

---


[![DOI](https://zenodo.org/badge/520046482.svg)](https://zenodo.org/badge/latestdoi/520046482)
![Testing](https://github.com/allfed/seaweed-upscaling-model/actions/workflows/testing.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


---


## Installation
To install the Seaweed Scale-Up Model package, we recommend setting up a virtual environment. This will ensure that the package and its dependencies are isolated from other projects on your machine, which can prevent conflicts and make it easier to manage your dependencies. Here are the steps to follow:

* Create a virtual environment using either conda by running the command `conda env create -f environment.yml`. This will create an environment called "seaweed_scale_up_model". A virtual environment is like a separate Python environment, which you can think of as a separate "room" for your project to live in, it's own space which is isolated from the rest of the system, and it will have it's own set of packages and dependencies, that way you can work on different projects with different versions of packages without interfering with each other.

* Activate the environment by running `conda activate seaweed_scale_up_model`. This command will make the virtual environment you just created the active one, so that when you run any python command or install any package, it will do it within the environment.

* Install the package by running `pip install -e .` in the main folder of the repository. This command will install the package you are currently in as a editable package, so that when you make changes to the package, you don't have to reinstall it again.

* If you want to run the example Jupyter notebook, you'll need to create a kernel for the environment. First, install the necessary tools by running `conda install -c anaconda ipykernel`. This command will install the necessary tools to create a kernel for the Jupyter notebook. A kernel is a component of Jupyter notebook that allows you to run your code. It communicates with the notebook web application and the notebook document format to execute code and display the results.

* Then, create the kernel by running `python -m ipykernel install --user --name=seaweed_scale_up_model`. This command will create a kernel with the name you specified "seaweed_scale_up_model" , which you can use to run the example notebook or play around with the model yourself.

You can now use the kernel "seaweed_scale_up_model" to run the example notebook or play around with the model yourself. If you are using the kernel and it fails due an import error for the model package, you might have to rerun: `pip install -e .`.

If you encounter any issues, feel free to open an issue in the repository.

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




