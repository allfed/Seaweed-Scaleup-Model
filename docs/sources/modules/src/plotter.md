#


### plot_satisfaction_results
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L15)
```python
.plot_satisfaction_results(
   clusters, percent_need
)
```

---
Plots the results of the model

**Arguments**

* **cluster_df** (pd.DataFrame) : The results of the model
* **percent_need** (int) : The percent of the population that needs to be satisfied


**Returns**

None, but plots and saves the results

----


### plot_area_results
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L74)
```python
.plot_area_results(
   clusters
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
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/plotter.py/#L108)
```python
.plot_self_shading()
```

---
Plots the self shading used in the model. Based on James and Boriah (2010).

**Arguments**

None

**Returns**

None
