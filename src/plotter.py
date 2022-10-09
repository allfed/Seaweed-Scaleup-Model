import matplotlib.pyplot as plt
import pandas as pd


def plot_satisfaction_results(self):
    """
    Plots the results of the model
    """
    counter = 0
    satisfied_need_df = pd.DataFrame()
    # Iterate over all growth rate results and plot them
    for growth_rate, results in self.growth_rate_results.items():
        df = results[0]
        food = df.loc[:, ["harvest_for_food", "harvest_intervall"]]
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
        food["daily_need"] = self.parameters["seaweed_needed"]
        food["daily_need_satisfied"] = (
            food["mean_daily_harvest"] / food["daily_need"]
        ) * 100
        satisfied_need_df[growth_rate] = food["daily_need_satisfied"]
        counter += 1

    ax = satisfied_need_df.plot()
    legend = ax.legend()
    legend.set_title("Growth Rate [%]")
    ax.set_xlabel("Days since start")
    ax.set_ylabel("% need satisfied")
    ax.set_title(
        "Calorie need satisfaction by growth rate\nScenario: "
        + str(self.parameters["calories_from_seaweed"])
        + " % of global calories from seaweed"
    )
    fig = plt.gcf()
    fig.set_size_inches(9, 4)
    plot_nicer(ax)
    plt.savefig("results/food_satisfaction.png", dpi=200, bbox_inches="tight")

def plot_area_results(self):
    """
    Plots how much area the different growth rates need
    """
    growth_area_df = pd.DataFrame(columns=["area"])
    for growth_rate in self.growth_rate_results.keys():
        growth_area_df.loc[growth_rate, "area"] = self.growth_rate_results[
            growth_rate
        ][1]
    ax = growth_area_df.plot(kind="barh", legend=False, zorder=5)
    ax.set_xlabel("Area [km²]")
    ax.set_ylabel("Growth Rate [%]")
    ax.set_title(
        "Area needed for different growth rates\nScenario: "
        + str(self.parameters["calories_from_seaweed"])
        + " % of global calories from seaweed"
    )
    plot_nicer(ax, with_legend=False)
    for tick in ax.get_xticklabels():
        tick.set_rotation(360)
    ax.yaxis.grid(False)
    ax.xaxis.get_offset_text().set_color("white")

    fig = plt.gcf()
    fig.set_size_inches(10, 3)
    plt.savefig("results/area.png", dpi=200, bbox_inches="tight")


def plot_nicer(ax, with_legend=True):
    """Takes an axis objects and makes it look nicer"""
    alpha = 0.7
    # Remove borders
    for spine in ax.spines.values():
        spine.set_visible(False)
    # Make text grey
    plt.setp(ax.get_yticklabels(), alpha=alpha)
    plt.setp(ax.get_xticklabels(), alpha=alpha)
    ax.set_xlabel(ax.get_xlabel(), alpha=alpha)
    ax.set_ylabel(ax.get_ylabel(), alpha=alpha)
    ax.set_title(ax.get_title(), alpha=alpha)
    ax.tick_params(axis="both", which="both", length=0)
    if with_legend:
        legend = ax.get_legend()
        for text in legend.get_texts():
            text.set_color("#676767")
        legend.get_title().set_color("#676767")
    ax.yaxis.get_offset_text().set_color("#676767")
    # Add a grid
    ax.grid(True, color="lightgrey", zorder=0)