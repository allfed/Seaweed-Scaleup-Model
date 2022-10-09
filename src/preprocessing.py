"""
Prepares the output of the growth model to be used in the upscaling model
"""
import os
import pandas as pd


def prep_data(path, cluster):
    """
    Changes the data from the growth model, so that it is a
    single time series for all the clusters.
    Args:
        path (str): path to the data
        cluster (int): the cluster number
    Returns:
        None, only writes to a csv
    """
    growth_df = pd.read_pickle(path + os.sep + "growth_df_clustered.pkl")
    median_growth_cluster = growth_df.groupby("cluster").median()
    clusters = []
    for cluster in median_growth_cluster.index:
        cluster_df = pd.DataFrame(median_growth_cluster.loc[cluster,:])
        cluster_df.columns = ["growth_rate_month"]
        cluster_df["month"] = cluster_df.index
        cluster_df_daily = pd.concat([cluster_df]*30).assign(growth_rate_daily=lambda x: x['growth_rate_month']).sort_values('month')
        cluster_df_daily.reset_index(inplace=True, drop=True)
        cluster_df_daily = cluster_df_daily["growth_rate_daily"]
        clusters.append(cluster_df_daily)
    all_clusters_daily = pd.concat(clusters,axis=1)
    all_clusters_daily.columns = ["growth_daily_cluster_" + str(cluster) for cluster in median_growth_cluster.index]
    all_clusters_daily.to_csv(path + os.sep + "actual_growth_rate_by_cluster.csv")


if __name__ == "__main__":
    path = "data"
    cluster = 0
    prep_data(path, cluster)
