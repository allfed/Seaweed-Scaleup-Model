"""
Prepares the output of the growth model to be used in the upscaling model
"""
import os

import pandas as pd


def prep_data(scenario, location, num_clusters, starting_month=0, max_growth=30):
    """
    Changes the data from the growth model, so that it is a
    single time series for all the clusters.

    The data at this point is still in fraction of maximum growth rate and not in % per day

    Arguments:
        path (str): path to the data
    Returns:
        None, only writes to a csv
    """
    growth_df = pd.read_pickle(
        "data"
        + os.sep
        + location
        + os.sep
        + scenario
        + os.sep
        + "seaweed_growth_rate_clustered_"
        + location
        + ".pkl"
    )
    median_growth_cluster = growth_df.groupby("cluster").median()
    clusters = []
    for cluster in range(num_clusters):
        cluster_df = pd.DataFrame(median_growth_cluster.loc[cluster, :])
        cluster_df.columns = ["growth_rate_month"]
        cluster_df["month"] = cluster_df.index
        # Only use the months after the nuclear war started
        cluster_df = cluster_df[cluster_df["month"] >= starting_month]
        cluster_df_daily = (
            pd.concat([cluster_df] * max_growth)
            .assign(growth_rate_daily=lambda x: x["growth_rate_month"])
            .sort_values("month")
        )
        cluster_df_daily.reset_index(inplace=True, drop=True)
        cluster_df_daily = cluster_df_daily["growth_rate_daily"]
        clusters.append(cluster_df_daily)
    all_clusters_daily = pd.concat(clusters, axis=1)
    all_clusters_daily.columns = [
        "growth_daily_cluster_" + str(cluster + 1)
        for cluster in median_growth_cluster.index
    ]
    all_clusters_daily.to_csv(
        "data"
        + os.sep
        + location
        + os.sep
        + scenario
        + os.sep
        + "actual_growth_rate_by_cluster.csv"
    )


if __name__ == "__main__":
    prep_data("150tg", "AUS", 2)
