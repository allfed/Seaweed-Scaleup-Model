#


## SeaweedUpscalingModel
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L9)
```python 
SeaweedUpscalingModel(
   path, cluster, initial_seaweed = 1000, initial_area_built = 1000,
   initial_area_used = 1000, min_density = 400, max_density = 4000, initial_lag = 0,
   max_area = 1000000, additional_saturation_time = 1.1, calories_from_seaweed = 20
)
```


---
Class that loads the data, calculates the scaleup


**Methods:**


### .load_literature_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L61)
```python
.load_literature_parameters(
   path
)
```

---
Load the parameters we found resonable values for from the file

### .load_growth_timeseries
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L73)
```python
.load_growth_timeseries(
   path, cluster
)
```

---
Loads the growth timeseries from the file

### .calculate_basic_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L82)
```python
.calculate_basic_parameters()
```

---
Calls all the other functinos for basic parametesr

### .calculate_global_food_demand_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L93)
```python
.calculate_global_food_demand_parameters()
```

---
Calculates the global demand for food

### .calculate_seaweed_farm_design_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L110)
```python
.calculate_seaweed_farm_design_parameters()
```

---
Calculates the parameters needed to built a seaweed farm

### .calculate_seaweed_farm_design_per_km2_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L123)
```python
.calculate_seaweed_farm_design_per_km2_parameters()
```

---
Calculates the material needed to construct a seaweed farm per km2

### .calculate_synthetic_fiber_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L163)
```python
.calculate_synthetic_fiber_parameters()
```

---
Calculates the synthetic fiber parameters

### .calculate_scaling_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L171)
```python
.calculate_scaling_parameters()
```

---
Calculates the parameters needed for scaling up the farms

### .calculate_rope_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L180)
```python
.calculate_rope_parameters()
```

---
Calculates the parameters for the rope machinery

### .seaweed_growth
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L223)
```python
.seaweed_growth(
   harvest_loss, initial_seaweed, initial_area_built, initial_area_used,
   new_module_area_per_day, min_density, max_density, max_area,
   optimal_growth_rate, growth_rate_fraction, initial_lag,
   percent_usable_for_growth, days_to_run
)
```

---
Calculates the seaweed growth and creatss a dataframe of all important
growth numbers

**Arguments**

* **harvest_loss**  : The loss of harvest due to harvesting
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
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L355)
```python
.determine_average_productivity(
   growth_rate_fraction, days_to_run
)
```

---
Let the model run for one km² to determine the productivity
per area and day and the harvest intervall
