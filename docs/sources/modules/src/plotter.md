#


### plot_satisfaction_results
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L16)
```python
.plot_satisfaction_results(
   clusters, percent_need, scenario, location
)
```

---
Plots the results of the model

**Arguments**

* **cluster_df** (pd.DataFrame) : The results of the model
* **percent_need** (int) : The percent of the population that needs to be satisfied
* **scenario** (str) : The scenario name


**Returns**

None, but plots and saves the results

----


### plot_scenario_comparison
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L86)
```python
.plot_scenario_comparison(
   percent_need, scenario_max_growth_rates_df, location
)
```

---
Plots the results of the model from all scenarios and compares the
cluster with the highest growth rate for a given scenario.

**Arguments**

* **percent_need** (int) : The percent of the population that needs to be satisfied


**Returns**

None, but plots and saves the results

----


### plot_area_results
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L240)
```python
.plot_area_results(
   clusters, scenario, location
)
```

---
Plots how much area the different growth rates need

**Arguments**

* **clusters** (dict) : The seaweed scale up area results sorted by cluster


**Returns**

None, but plots and saves the results

----


### plot_self_shading
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L278)
```python
.plot_self_shading()
```

---
Plots the self shading used in the model. Based on James and Boriah (2010).

**Arguments**

None

**Returns**

None

----


### create_plots
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L311)
```python
.create_plots(
   location, scenarios, consumption_aim, number_of_clusters,
   with__shading = False, with_comparison = True
)
```

---
Main function to run the plotter and read the data

**Arguments**

* **location** (str) : The location to plot
* **consumption_aim** (float) : The consumption aim in percent
* **with_self_shading** (bool) : Whether to plot the self shading factor
* **with_comparison** (bool) : Whether to plot the scenario comparison


**Returns**

None
