import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

from src.scaleup_model import self_shading

plt.style.use(
    "https://raw.githubusercontent.com/allfed/ALLFED-matplotlib-style-sheet/main/ALLFED.mplstyle"
)


def plot_satisfaction_results(clusters, percent_need):
    """
    Plots the results of the model
    Arguments:
        cluster_df (pd.DataFrame): The results of the model
        percent_need (int): The percent of the population that needs to be satisfied
    Returns:
        None, but plots and saves the results
    """
    counter = 0
    satisfied_need_df = pd.DataFrame()
    # Iterate over all growth rate results and plot them
    for cluster, cluster_df in clusters.items():
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
        satisfied_need_df["Cluster " + str(cluster + 1) + " Mean Harvest Day"] = food[
            "mean_daily_harvest"
        ]
        counter += 1
    # Convert to months
    satisfied_need_df.index = satisfied_need_df.index / 30
    ax = satisfied_need_df[["Cluster " + str(i) for i in [1, 3]]].plot(
        color="black", linewidth=2.5, legend=False
    )
    ax = satisfied_need_df[["Cluster " + str(i) for i in [1, 3]]].plot(
        color=["#95c091", "#3A913F"],
        linewidth=2,
        ax=ax,
        label=["Cluster 1", "Cluster 3"],
    )
    ax.axhline(y=percent_need, color="dimgrey", alpha=0.5, zorder=0)
    ax.set_xlabel("Months since Nuclear War")
    ax.set_ylabel("% Global Calories by Seaweed")
    fig = plt.gcf()
    fig.set_size_inches(9, 4)
    plt.savefig("results/food_satisfaction.png", dpi=300, bbox_inches="tight")
    satisfied_need_df.to_csv("results/food_satisfaction.csv")
    plt.close()


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
    areas.reset_index(inplace=True)
    areas.columns = ["Cluster", "Area [km²]"]
    ax = areas.plot(
        kind="barh",
        y="Area [km²]",
        x="Cluster",
        legend=False,
        color=("#95c091", "#3A913F"),
    )
    # Format the x tick labels with a thousand separator
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax.set_xlabel("Area [km²]")
    ax.set_ylabel("Cluster")
    ax.yaxis.grid(False)
    fig = plt.gcf()
    fig.set_size_inches(10, 3)
    plt.savefig("results/area.png", dpi=250, bbox_inches="tight")
    plt.close()


def plot_self_shading():
    """
    Plots the self shading used in the model. Based on James and Boriah (2010).
    Arguments:
        None
    Returns:
        None
    """
    # Creates the x-axis
    x = np.linspace(0.01, 10, 10000)
    # Creates the y-axis
    y = [self_shading(i) for i in x]
    # Plots the results
    plt.plot(x, y, linewidth=2.5, color="black")
    plt.plot(x, y, linewidth=2)
    # Adds the unit to the y-axis
    plt.ylabel("Self-Shading Factor")
    # Adds the unit to the x-axis
    plt.xlabel("Density [kg/m²]")
    # Change the size
    plt.gcf().set_size_inches(8, 2)
    # Saves the plot
    plt.savefig(
        "results" + os.sep + "self_shading_factor.png",
        dpi=250,
        bbox_inches="tight",
    )
    # Closes the plot
    plt.close()


def main():
    """
    Main function to run the plotter and read the data
    Arguments:
        None
    Returns:
        None
    """
    clusters = {}
    for cluster in [0, 2]:
        clusters[cluster] = pd.read_csv(
            "results" + os.sep + "harvest_df_cluster_" + str(cluster) + ".csv"
        )
    plot_area_results(clusters)
    plot_satisfaction_results(clusters, 70)
    plot_self_shading()


if __name__ == "__main__":
    main()
