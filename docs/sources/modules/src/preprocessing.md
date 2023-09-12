#


### prep_data
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/preprocessing.py/#L9)
```python
.prep_data(
   scenario, location, num_clusters, starting_month = 0, max_growth = 30
)
```

---
Changes the data from the growth model, so that it is a
single time series for all the clusters.

The data at this point is still in fraction of maximum growth rate and not in % per day


**Arguments**

* **path** (str) : path to the data


**Returns**

None, only writes to a csv
