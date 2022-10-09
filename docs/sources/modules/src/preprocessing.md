#


### prep_data
[source](https://github.com/allfed/Seaweed-Upscaling-Model/blob/master/src/preprocessing.py/#L8)
```python
.prep_data(
   path, cluster
)
```

---
Changes the data from the growth model, so that it is a
single time series for all the clusters.

**Args**

* **path** (str) : path to the data
* **cluster** (int) : the cluster number


**Returns**

None, only writes to a csv
