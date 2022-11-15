import os

import matplotlib.pyplot as plt
import pandas as pd

plt.style.use(
    "https://raw.githubusercontent.com/allfed/ALLFED-matplotlib-style-sheet/main/ALLFED.mplstyle"
)


def plot_satisfaction_results(cluster_df, percent_need):
    """
    Plots the results of the model
    Arguments:
        cluster_df (pd.DataFrame): The results of the model
    Returns:
        None, but plots and saves the results
    """
    counter = 0
    satisfied_need_df = pd.DataFrame()
    # Iterate over all growth rate results and plot them
    for cluster, cluster_df in cluster_df.items():
        food = cluster_df.loc[
            :, ["harvest_for_food", "harvest_intervall", "seaweed_needed_per_day"]
        ]
        # backfill to calulcate averages
        food["harvest_for_food"].interpolate(
            "zero", fill_value=0, limit_direction="backward", inplace=True
        )
        food["harvest_intervall"].fillna(method="backfill", inplace=True)
        food.fillna(method="ffill", inplace=True)
        # Calculate the food needed
        food["mean_daily_harvest"] = (
            food["harvest_for_food"] / food["harvest_intervall"]
        )
        food["daily_need"] = food["seaweed_needed_per_day"]
        food["daily_need_satisfied"] = (
            food["mean_daily_harvest"] / food["daily_need"]
        ) * 100
        daily_need_satisfied = food["daily_need_satisfied"].rolling(20).mean()
        # Convert back to the 30 % of the need
        daily_need_satisfied = (daily_need_satisfied / 100) * percent_need
        satisfied_need_df["Cluster " + str(cluster + 1)] = daily_need_satisfied
        counter += 1

    satisfied_need_df.index = satisfied_need_df.index / percent_need
    ax = satisfied_need_df.plot(color="black", linewidth=2.5, legend=False)
    ax = satisfied_need_df.plot(
        color=["#31688e", "#35b779", "#fde725"], linewidth=2, ax=ax
    )
    ax.axhline(y=30, color="dimgrey", alpha=0.5, zorder=0)
    ax.set_xlabel("Months since nuclear war")
    ax.set_ylabel("% global calories by seaweed")
    fig = plt.gcf()
    fig.set_size_inches(9, 4)
    plt.savefig("results/food_satisfaction.png", dpi=250, bbox_inches="tight")
    satisfied_need_df.to_csv("results/food_satisfaction.csv")


def plot_area_results(clusters):
    """
    Plots how much area the different growth rates need
    Arguments:
        clusters (dict): The seaweed scale up area results sorted by cluster
    Returns:
        None, but plots and saves the results
    """
    areas = {}
    for cluster, cluster_df in clusters.items():
        # Skip emtpy dfs
        if not cluster_df.empty:
            areas[cluster + 1] = cluster_df["max_area"].values[0]
    areas = pd.DataFrame.from_dict(areas, orient="index")
    ax = areas.plot(kind="barh", legend=False)
    ax.set_xlabel("Area [km²]")
    ax.set_ylabel("Cluster")
    ax.yaxis.grid(False)
    fig = plt.gcf()
    fig.set_size_inches(10, 3)
    plt.savefig("results/area.png", dpi=250, bbox_inches="tight")


def main():
    """
    Main function to run the plotter and read the data
    Returns:
        None
    """
    clusters = {}
    for cluster in range(1, 4, 1):
        clusters[cluster] = pd.read_csv(
            "results" + os.sep + "harvest_df_cluster_" + str(cluster) + ".csv"
        )
    plot_area_results(clusters)
    plot_satisfaction_results(clusters, 30)


if __name__ == "__main__":
    main()
