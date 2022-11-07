import matplotlib.pyplot as plt
import pandas as pd
import os
plt.style.use(
    "https://raw.githubusercontent.com/allfed/ALLFED-matplotlib-style-sheet/main/ALLFED.mplstyle")


def plot_satisfaction_results(cluster_df):
    """
    Plots the results of the model
    """
    counter = 0
    satisfied_need_df = pd.DataFrame()
    # Iterate over all growth rate results and plot them
    for cluster, cluster_df in clusters.items():
        food = cluster_df.loc[:, ["harvest_for_food", "harvest_intervall",
        "seaweed_needed_per_day"]]
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
        satisfied_need_df["Cluster " + str(cluster)] = food["daily_need_satisfied"].rolling(20).mean()
        counter += 1

    ax = satisfied_need_df.plot()
    legend = ax.legend()
    legend.set_title("Growth Rate [%]")
    ax.set_xlabel("Days since start")
    ax.set_ylabel("% need satisfied")
    fig = plt.gcf()
    fig.set_size_inches(9, 4)
    plt.savefig("results/food_satisfaction.png", dpi=200, bbox_inches="tight")


def plot_area_results(clusters):
    """
    Plots how much area the different growth rates need
    """
    areas = {}
    for cluster, cluster_df in clusters.items():
        # Skip emtpy dfs
        if not cluster_df.empty:
            areas[cluster+1] = cluster_df["max_area"].values[0]
    areas = pd.DataFrame.from_dict(areas, orient="index")
    ax = areas.plot(kind="barh", legend=False)
    ax.set_xlabel("Area [km²]")
    ax.set_ylabel("Cluster")
    ax.yaxis.grid(False)
    fig = plt.gcf()
    fig.set_size_inches(10, 3)
    plt.savefig("results/area.png", dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    clusters = {}
    for cluster in range(1, 4, 1):
        clusters[cluster] = pd.read_csv(
            "results" + os.sep + "harvest_df_cluster_" + str(cluster) + ".csv")
    plot_area_results(clusters)
    plot_satisfaction_results(clusters)

