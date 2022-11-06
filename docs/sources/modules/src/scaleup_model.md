#


## SeaweedUpscalingModel
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L10)
```python 
SeaweedUpscalingModel(
   path, cluster, calories_from_seaweed = 20
)
```


---
Class that loads the data, calculates the scaleup and saves it into a csv


**Methods:**


### .load_literature_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L31)
```python
.load_literature_parameters(
   path
)
```

---
Load the parameters we found resonable values for from the file

### .load_growth_timeseries
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L43)
```python
.load_growth_timeseries(
   path, cluster
)
```

---
Loads the growth timeseries from the file

### .calculate_global_food_demand_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L52)
```python
.calculate_global_food_demand_parameters()
```

---
Calculates the global demand for food

### .self_shading
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L69)
```python
.self_shading(
   density
)
```

---
Calculates how much the growth rate is reduced due to self shading.
Based on the publication:
James, S.C. and Boriah, V. (2010), Modeling algae growth
in an open-channel raceway
Journal of Computational Biology, 17(7), 895−906.
args:
density: the seaweed density
---
returns:
    the growth rate fraction

### .seaweed_growth
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L86)
```python
.seaweed_growth(
   initial_seaweed, initial_area_built, initial_area_used,
   new_module_area_per_day, min_density, max_density, max_area,
   optimal_growth_rate, growth_rate_fraction, initial_lag,
   percent_usable_for_growth, days_to_run
)
```

---
Calculates the seaweed growth and creatss a dataframe of all important
growth numbers

**Arguments**

* **initial_seaweed**  : The initial amount of seaweed
* **initial_area_built**  : The initial area built
* **initial_area_used**  : The initial area used
* **new_module_area_per_day**  : The area built per day
* **min_density**  : The minimum density
* **max_density**  : The maximum density
* **max_area**  : The maximum area
* **optimal_growth_rate**  : The optimal growth rate
* **growth_rate_fraction**  : The fraction of the growth rate (can either be scalar or list)
* **initial_lag**  : The initial lag
* **percent_usable_for_growth**  : The percent usable for growth
* **days_to_run**  : The number of days to run


**Returns**

A dataframe with all important growth numbers

### .determine_average_productivity
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L220)
```python
.determine_average_productivity(
   growth_rate_fraction, days_to_run
)
```

---
Let the model run for one km² to determine the productivity
per area and day and the harvest intervall

----


### run_model
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L259)
```python
.run_model()
```

