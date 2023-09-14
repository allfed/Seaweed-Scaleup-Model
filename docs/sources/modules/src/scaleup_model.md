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
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L31)
```python
.load_growth_timeseries(
   path, cluster
)
```

---
Loads the growth timeseries from the file

**Arguments**

* **path**  : the path to the timeseries
* **cluster**  : the cluster to use


**Returns**

None

### .seaweed_growth
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L47)
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
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L210)
```python
.determine_average_productivity(
   growth_rate_fraction, days_to_run, percent_usable_for_growth,
   optimal_growth_rate
)
```

---
Let the model run for one km² to determine the productivity
per area and day and the harvest intervall

**Arguments**

* **growth_rate_fraction**  : float or list of the growth rate of seaweed
* **days_to_run**  : int, number of days to run the model
* **percent_usable_for_growth**  : float, the percentage of the module area
    that can be used for growth
* **optimal_growth_rate**  : float, the optimal growth rate of the seaweed


**Returns**

* **productivity**  : float, the average productivity per km² and day


----


### self_shading
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L265)
```python
.self_shading(
   density
)
```

---
Calculates how much the growth rate is reduced due to self shading.
Based on the publication:
Lapointe, B. E., & Ryther, J. H. (1978).
Some aspects of the growth and yield of Gracilaria tikvahiae in culture.
Aquaculture, 15(3), 185-193. https://doi.org/10.1016/0044-8486(78)90030-3

**Arguments**

* **density**  : the seaweed density


**Returns**

the growth rate fraction

----


### calculate_seaweed_need
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L284)
```python
.calculate_seaweed_need(
   global_pop, calories_per_person_per_day, food_waste,
   calories_per_t_seaweed_wet, seaweed_limit
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
* **seaweed_limit** (float) : how large a fraction of the food can be substituted by seaweed


**Returns**

* **float**  : amount of seaweed needed to feed the population


----


### seaweed_farm_area_per_day
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L315)
```python
.seaweed_farm_area_per_day(
   day
)
```

---
Estimates the area that can be built per day
based on how many days have passed. This is a rough estimate
based on:
https://github.com/allfed/Seaweed-Scaleup-Model/blob/main/scripts/Logistic%20Growth.ipynb

**Arguments**

* **day**  : the day


**Returns**

the area that can be built per day

----


### logistic_curve
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L336)
```python
.logistic_curve(
   x, max_L, k, x0, off
)
```

---
Describes a logistic growth curve

**Arguments**

* **x**  : value to calculate
* **max_L**  : maximum value of the curve
* **k**  : the logistic growth rate
* **x0**  : the sigmoid's midpoint
* **off**  : offset to 0

---
Returns
    float: y value corresponding to x

----


### run_model
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/scaleup_model.py/#L351)
```python
.run_model(
   optimal_growth_rate, days_to_run, global_pop, calories_per_person_per_day,
   harvest_loss, food_waste, calories_per_t_seaweed_wet, food_limit, feed_limit,
   biofuel_limit, percent_usable_for_growth, scenarios, location,
   number_of_clusters
)
```

---
Run the model

**Arguments**

* **optimal_growth_rate** (float) : the optimal growth rate
* **days_to_run** (int) : the number of days to run the model
* **global_pop** (int) : Global population
* **calories_per_person_per_day** (int) : Calories needed per person per day
* **harvest_loss** (float) : Fraction of harvest lost
* **food_waste** (float) : Fraction of food wasted
* **calories_per_kg_seaweed** (int) : Calories per t of seaweed
* **food_limit** (float) : how large a fraction of the food can be substituted by seaweed
* **feed_limit** (float) : how large a fraction of the feed can be substituted by seaweed
* **biofuel_limit** (float) : how large a fraction of the biofuel can be substituted by seaweed
* **percent_usable_for_growth** (float) : how much of the harvest is usable for growth
* **scenarios** (list) : list of scenarios to run
* **location** (str) : location on the globe
* **number_of_clusters** (int) : number of clusters


**Returns**

None
