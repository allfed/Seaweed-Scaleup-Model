#


## SeaweedScaleUpModel
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L11)
```python 
SeaweedScaleUpModel(
   path, cluster, seaweed_need, harvest_loss
)
```


---
Class that loads the data, calculates the scaleup and saves it into a csv


**Methods:**


### .load_growth_timeseries
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L27)
```python
.load_growth_timeseries(
   path, cluster
)
```

---
Loads the growth timeseries from the file

### .self_shading
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L38)
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

**Arguments**

* **density**  : the seaweed density


**Returns**

the growth rate fraction

### .seaweed_growth
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L55)
```python
.seaweed_growth(
   initial_seaweed, initial_area_built, initial_area_used,
   new_module_area_per_day, min_density, max_density, max_area,
   optimal_growth_rate, growth_rate_fraction, initial_lag,
   percent_usable_for_growth, days_to_run, verbose = False
)
```

---
Calculates the seaweed growth and creatss a dataframe of all important
growth numbers

**Arguments**

* **initial_seaweed**  : The initial amount of seaweed in t
* **initial_area_built**  : The initial area built in km²
* **initial_area_used**  : The initial area used in km²
* **new_module_area_per_day**  : The area built per day in km²
* **min_density**  : The minimum density in t/km²
* **max_density**  : The maximum density in t/km²
* **max_area**  : The maximum area in km²
* **optimal_growth_rate**  : The optimal growth rate in %
* **growth_rate_fraction**  : The fraction of the growth rate (can either be scalar or list)
* **initial_lag**  : The initial lag in days
* **percent_usable_for_growth**  : The percent usable for growth in %
* **days_to_run**  : The number of days to run


**Returns**

A dataframe with all important growth numbers

### .determine_average_productivity
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L202)
```python
.determine_average_productivity(
   growth_rate_fraction, days_to_run, percent_usable_for_growth
)
```

---
Let the model run for one km² to determine the productivity
per area and day and the harvest intervall

----


### calculate_seaweed_need
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L245)
```python
.calculate_seaweed_need(
   global_pop, calories_per_person_per_day, food_waste,
   calories_per_t_seaweed_wet, iodine_limit
)
```

---
Calculates the amount of seaweed needed to feed the population
based on global population and the amount of seaweed needed per person
limited by the iodine content of the seaweed

**Arguments**

* **global_pop** (int) : Global population
* **calories_per_person_per_day** (int) : Calories needed per person per day
* **food_waste** (float) : Fraction of food wasted
* **calories_per_kg_seaweed** (int) : Calories per t of seaweed
* **iodine_limit** (float) : how large a fraction of the food can be substituted by seaweed


**Returns**

* **float**  : amount of seaweed needed to feed the population


----


### run_model
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L276)
```python
.run_model()
```

