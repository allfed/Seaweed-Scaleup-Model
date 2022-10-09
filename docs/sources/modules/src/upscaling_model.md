#


## SeaweedUpscalingModel
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L9)
```python 
SeaweedUpscalingModel(
   path, cluster, initial_seaweed = 1000, initial_area_built = 1000,
   initial_area_used = 1000, min_density = 400, max_density = 4000, initial_lag = 0,
   max_area = 1000000, additional_saturation_time = 1.1, calories_from_seaweed = 20
)
```


---
Class that loads the data, calculates the upscaling and plots it


**Methods:**


### .load_literature_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L61)
```python
.load_literature_parameters(
   path
)
```

---
Load the parameters we found resonable values for from the file

### .load_growth_timeseries
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L73)
```python
.load_growth_timeseries(
   path, cluster
)
```

---
Loads the growth timeseries from the file

### .calculate_basic_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L80)
```python
.calculate_basic_parameters()
```

---
Calls all the other functinos for basic parametesr

### .calculate_global_food_demand_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L91)
```python
.calculate_global_food_demand_parameters()
```

---
Calculates the global demand for food

### .calculate_seaweed_farm_design_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L108)
```python
.calculate_seaweed_farm_design_parameters()
```

---
Calculates the parameters needed to built a seaweed farm

### .calculate_seaweed_farm_design_per_km2_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L121)
```python
.calculate_seaweed_farm_design_per_km2_parameters()
```

---
Calculates the material needed to construct a seaweed farm per km2

### .calculate_synthetic_fiber_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L161)
```python
.calculate_synthetic_fiber_parameters()
```

---
Calculates the synthetic fiber parameters

### .calculate_scaling_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L169)
```python
.calculate_scaling_parameters()
```

---
Calculates the parameters needed for scaling up the farms

### .calculate_rope_parameters
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L178)
```python
.calculate_rope_parameters()
```

---
Calculates the parameters for the rope machinery

### .seaweed_growth
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L221)
```python
.seaweed_growth(
   harvest_loss, initial_seaweed, initial_area_built, initial_area_used,
   new_module_area_per_day, min_density, max_density, max_area,
   optimal_growth_rate, initial_lag, percent_usable_for_growth, days_to_run
)
```

---
Calculates the seaweed growth and creatss a dataframe of all important
growth numbers

### .determine_average_productivity
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/upscaling_model.py/#L325)
```python
.determine_average_productivity(
   optimal_growth_rate, harvest_loss, min_density, max_density,
   percent_usable_for_growth, days_to_run
)
```

---
Let the model run for one km² to determine the productivity
per area and day and the harvest intervall
