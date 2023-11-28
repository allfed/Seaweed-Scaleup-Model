import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from src.scaleup_model import self_shading

plt.style.use(
    "https://raw.githubusercontent.com/allfed/ALLFED-matplotlib-style-sheet/main/ALLFED.mplstyle"
)


def plot_satisfaction_results(clusters, percent_need, scenario, location):
    """
    Plots the results of the model
    Arguments:
        cluster_df (pd.DataFrame): The results of the model
        percent_need (int): The percent of the population that needs to be satisfied
        scenario (str): The scenario name
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
        satisfied_need_df["Cluster " + str(cluster)] = daily_need_satisfied
        satisfied_need_df["Cluster " + str(cluster) + " Mean Harvest Day"] = food[
            "mean_daily_harvest"
        ]
        counter += 1
    available_clusters = ["Cluster " + str(i) for i in clusters.keys()]
    # Convert to months
    satisfied_need_df.index = satisfied_need_df.index / 30
    ax = satisfied_need_df[available_clusters].plot(
        color="black", linewidth=2.5, legend=False
    )
    ax = satisfied_need_df[available_clusters].plot(
        color=["#95c091", "#3A913F", "grey"],
        linewidth=2,
        ax=ax,
        label=available_clusters,
    )
    ax.axhline(y=percent_need, color="dimgrey", alpha=0.5, zorder=0)
    ax.set_xlabel("Months since Nuclear War")
    ax.set_ylabel("Percent of Human Food Demand")
    # reformat scenario from 5tg to 5 Tg
    scenario_reformat = scenario.replace("tg", " Tg")
    ax.set_title("Scenario " + scenario_reformat)
    fig = plt.gcf()
    fig.set_size_inches(9, 4)
    plt.savefig(
        "results"
        + os.sep
        + location
        + os.sep
        + scenario
        + os.sep
        + "food_satisfaction.png",
        dpi=300,
        bbox_inches="tight",
    )
    satisfied_need_df.to_csv(
        "results"
        + os.sep
        + location
        + os.sep
        + scenario
        + os.sep
        + "food_satisfaction.csv"
    )
    plt.close()


def plot_scenario_comparison(percent_need, scenario_max_growth_rates_df, location):
    """
    Plots the results of the model from all scenarios and compares the
    cluster with the highest growth rate for a given scenario.
    Arguments:
        percent_need (int): The percent of the population that needs to be satisfied
    Returns:
        None, but plots and saves the results
    """
    # Define the colors starting with #3A913F for the 150 tg scenario
    # and adding 6 very distinct green colors
    colors = {
        "150 Tg": "#3A913F",
        "47 Tg": "#5DAF5D",
        "37 Tg": "#7FC17F",
        "27 Tg": "#A1DCA1",
        "16 Tg": "#C3F5C3",
        "5 Tg": "#E6FFE6",
        "Control": "#95c091",
    }

    # Create a figure to plot in
    fig, ax = plt.subplots(1, 1)
    # Iterate over all scenarios
    for scenario in ["control"] + [str(i) + "tg" for i in [5, 16, 27, 37, 47, 150]]:
        # Find the cluster with the highest growth rate
        scenario_growth = scenario_max_growth_rates_df[
            scenario_max_growth_rates_df["scenario"] == scenario
        ]
        max_growth_rate_index = scenario_growth["max_growth_rate"].idxmax()
        max_growth_rate_cluster = scenario_growth.loc[max_growth_rate_index, "cluster"]
        # Read in the results for the cluster with the highest growth rate
        cluster_df = pd.read_csv(
            "results"
            + os.sep
            + location
            + os.sep
            + scenario
            + os.sep
            + "harvest_df_cluster_"
            + str(max_growth_rate_cluster)
            + ".csv"
        )
        # Calculate the food needed
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

        # Convert to months
        daily_need_satisfied.index = daily_need_satisfied.index / 30
        # Plot the results
        ax = daily_need_satisfied.plot(color="black", linewidth=2.5, label=None, ax=ax)
        if scenario != "control":
            scenario = scenario.replace("tg", " Tg")
        else:
            scenario = "Control"
        ax = daily_need_satisfied.plot(
            color=colors[scenario],
            linewidth=2,
            ax=ax,
        )
    # Create a custom legend
    legend_elements = [
        Line2D(
            [0],
            [0],
            color=colors["150 Tg"],
            lw=2,
            label="150 Tg",
        ),
        Line2D(
            [0],
            [0],
            color=colors["47 Tg"],
            lw=2,
            label="47 Tg",
        ),
        Line2D(
            [0],
            [0],
            color=colors["37 Tg"],
            lw=2,
            label="37 Tg",
        ),
        Line2D(
            [0],
            [0],
            color=colors["27 Tg"],
            lw=2,
            label="27 Tg",
        ),
        Line2D(
            [0],
            [0],
            color=colors["16 Tg"],
            lw=2,
            label="16 Tg",
        ),
        Line2D(
            [0],
            [0],
            color=colors["5 Tg"],
            lw=2,
            label="5 Tg",
        ),
        Line2D(
            [0],
            [0],
            color=colors["Control"],
            lw=2,
            label="Control",
        ),
    ]
    ax.legend(handles=legend_elements)
    ax.axhline(y=percent_need, color="dimgrey", alpha=0.5, zorder=0)
    # Annotate the line for 150 Tg
    ax.annotate(
        r"$\longleftarrow$ 150 Tg",
        xy=(90, 37),
        xytext=(90, 37),
        xycoords="data",
        textcoords="data",
        fontsize=7,
        color="dimgrey",
        horizontalalignment="left",
        verticalalignment="bottom",
    )
    ax.set_xlabel("Months since Nuclear War")
    ax.set_ylabel("Percent of Human Food Demand")
    fig = plt.gcf()
    fig.set_size_inches(9, 4)
    plt.savefig(
        "results" + os.sep + location + os.sep + "scenario_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def plot_area_results(clusters, scenario, location):
    """
    Plots how much area the different growth rates need
    Arguments:
        clusters (dict): The seaweed scale up area results sorted by cluster
    Returns:
        None, but plots and saves the results
    """
    areas_dict = {}
    for cluster, cluster_df in clusters.items():
        # Skip emtpy dfs
        if not cluster_df.empty:
            areas_dict[cluster] = cluster_df["max_area"].values[0]
    areas = pd.DataFrame.from_dict(areas_dict, orient="index")
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
    plt.savefig(
        "results" + os.sep + location + os.sep + scenario + os.sep + "area.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def plot_self_shading():
    """
    Plots the self shading used in the model. Based on James and Boriah (2010).
    Arguments:
        None
    Returns:
        None
    """
    # Create a new figure
    fig, ax = plt.subplots(1, 1)
    # Creates the x-axis
    x = np.linspace(0.01, 10, 10000)
    # Creates the y-axis
    y = [self_shading(i) for i in x]
    # Plots the results
    ax.plot(x, y, linewidth=2.5, color="black")
    ax.plot(x, y, linewidth=2)
    # Adds the unit to the y-axis
    ax.set_ylabel("Self-Shading Factor")
    # Adds the unit to the x-axis
    ax.set_xlabel("Density [kg/m²]")
    # Change the size
    fig.set_size_inches(8, 2)
    # Saves the plot
    plt.savefig(
        "results" + os.sep + "self_shading_factor.png",
        dpi=250,
        bbox_inches="tight",
    )
    # Closes the plot
    plt.close()


def create_plots(
    location,
    scenarios,
    consumption_aim,
    number_of_clusters,
    with_self_shading=False,
    with_comparison=True,
):
    """
    Main function to run the plotter and read the data
    Arguments:
        location (str): The location to plot
        consumption_aim (float): The consumption aim in percent
        with_self_shading (bool): Whether to plot the self shading factor
        with_comparison (bool): Whether to plot the scenario comparison
    Returns:
        None
    """
    # Make the overall comparison plot
    scenario_max_growth_rates_df = pd.read_csv(
        "results" + os.sep + location + os.sep + "scenario_max_growth_rates.csv"
    )
    if with_comparison:
        plot_scenario_comparison(
            consumption_aim, scenario_max_growth_rates_df, location
        )
    # Plot the results for all scenarios
    for scenario in scenarios:
        print("Plotting results for scenario " + scenario)
        clusters = {}
        for cluster in range(number_of_clusters+1):
            try:
                clusters[cluster] = pd.read_csv(
                    "results"
                    + os.sep
                    + location
                    + os.sep
                    + scenario
                    + os.sep
                    + "harvest_df_cluster_"
                    + str(cluster)
                    + ".csv"
                )
                print(
                    "Reading in results for cluster "
                    + str(cluster)
                    + " in scenario "
                    + scenario
                )
            except FileNotFoundError:
                print(
                    "No results for cluster "
                    + str(cluster)
                    + " in scenario "
                    + scenario
                )
        plot_area_results(clusters, scenario, location)
        plot_satisfaction_results(clusters, consumption_aim, scenario, location)
    if with_self_shading:
        plot_self_shading()
