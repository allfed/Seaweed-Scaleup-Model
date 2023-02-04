"""
Model to calculate the time it takes to scale-up global seaweed production
"""
import math
import os

import numpy as np
import pandas as pd


class SeaweedScaleUpModel:
    """
    Class that loads the data, calculates the scaleup and saves it into a csv
    """

    def __init__(self, path, cluster, seaweed_need, harvest_loss):
        """
        Initialize the model
        Arguments:
            path: the path to the data
            cluster: the cluster to use
            seaweed_need: the amount of seaweed needed
            harvest_loss: the harvest loss in percent
        Returns:
            None
        """
        self.seaweed_need = seaweed_need
        self.harvest_loss = harvest_loss
        self.load_growth_timeseries(path, cluster)

    def load_growth_timeseries(self, path, cluster):
        """
        Loads the growth timeseries from the file
        Arguments:
            path: the path to the timeseries
            cluster: the cluster to use
        Returns:
            None
        """
        growth_timeseries = pd.read_csv(
            path + os.sep + "actual_growth_rate_by_cluster.csv"
        )
        self.growth_timeseries = growth_timeseries[
            "growth_daily_cluster_" + str(cluster)
        ].to_list()

    def seaweed_growth(
        self,
        initial_seaweed,
        initial_area_built,
        initial_area_used,
        new_module_area_per_day,
        min_density,
        max_density,
        max_area,
        optimal_growth_rate,
        growth_rate_fraction,
        initial_lag,
        percent_usable_for_growth,
        days_to_run,
        verbose=False,
    ):
        """
        Calculates the seaweed growth and creatss a dataframe of all important
        growth numbers
        Arguments:
            initial_seaweed: The initial amount of seaweed in t
            initial_area_built: The initial area built in km²
            initial_area_used: The initial area used in km²
            new_module_area_per_day: The area built per day in km²
            min_density: The minimum density in t/km²
            max_density: The maximum density in t/km²
            max_area: The maximum area in km²
            optimal_growth_rate: The optimal growth rate in %
            growth_rate_fraction: The fraction of the growth rate (can either be scalar or list)
            initial_lag: The initial lag in days
            percent_usable_for_growth: The percent usable for growth in %
            days_to_run: The number of days to run
        Returns:
            A dataframe with all important growth numbers
        """
        # Initialize
        current_area_built = initial_area_built
        current_area_used = initial_area_used
        current_seaweed = initial_seaweed
        current_density = current_seaweed / current_area_used

        cumulative_harvest_for_food = 0
        current_seaweed_need = 0
        harvest_intervall = 0
        # collect all the harvest_intervall values to find the most common at the end
        harvest_intervall_all = []
        df = pd.DataFrame(index=range(days_to_run))
        for current_day in range(days_to_run):
            # Calculate the area that can be built on that day
            # Check if it is larger than 0, because this means that
            # the model is running to estimate the productivity on a fixed area
            if new_module_area_per_day > 0:
                new_module_area_per_day = seaweed_farm_area_per_day(current_day)
            # We can only use a fraction of the module area to grow seaweed
            growth_area_per_day = new_module_area_per_day * (
                percent_usable_for_growth / 100
            )
            # Skip days that are needed to coordinate production
            if current_day > initial_lag:
                # Build more seaweed farms if maximum is not reached
                if current_area_built < max_area:
                    df.loc[
                        current_day, "new_module_area_per_day"
                    ] = new_module_area_per_day
                    current_area_built += growth_area_per_day
                    if current_area_built > max_area:
                        current_area_built = max_area
                else:
                    df.loc[current_day, "new_module_area_per_day"] = 0
            else:
                df.loc[current_day, "new_module_area_per_day"] = 0
            self_shading_factor = self_shading(
                current_density / 1000
            )  # convert to kg/m² from t/km2
            # Let the seaweed grow
            # This can be done with a fixed value for the growth rate fraction
            # or with a timeseries of the growth rate fraction
            if isinstance(growth_rate_fraction, float):
                actual_growth_rate = 1 + (
                    (optimal_growth_rate * growth_rate_fraction * self_shading_factor)
                    / 100
                )
            elif isinstance(growth_rate_fraction, list):
                actual_growth_rate = 1 + (
                    (
                        optimal_growth_rate
                        * growth_rate_fraction[current_day]
                        * self_shading_factor
                    )
                    / 100
                )
            else:
                raise TypeError("growth_rate_fraction must be float or list")
            current_seaweed = current_seaweed * actual_growth_rate
            # Calculate the seaweed density, so we know when to harvest
            current_density = current_seaweed / current_area_used
            # Check if we have reached harvest density
            if current_density >= max_density:
                if verbose:
                    print("harvesting at day ", current_day)
                    print("days since last harvest: ", harvest_intervall)
                df.loc[current_day, "harvest_intervall"] = harvest_intervall
                harvest_intervall_all.append(harvest_intervall)
                harvest_intervall = 0
                # calculate the amount of seaweed we have to leave in the field
                seaweed_remaining_to_grow = current_area_used * min_density
                df.loc[
                    current_day, "seaweed_remaining_to_grow"
                ] = seaweed_remaining_to_grow
                # calulate the amount harvested
                harvest_wet = current_seaweed - seaweed_remaining_to_grow
                df.loc[current_day, "harvest_wet"] = harvest_wet
                if verbose:
                    print("harvest_wet", harvest_wet)
                # calculate harvest loss
                # make it a fraction
                harvest_loss = self.harvest_loss / 100
                assert harvest_loss <= 1 and harvest_loss >= 0
                harvest_wet_with_loss = harvest_wet * (1 - harvest_loss)
                df.loc[current_day, "harvest_wet_with_loss"] = harvest_wet_with_loss
                # calculate how much seaweed we would need to stock all aready built area
                current_seaweed_need = (
                    current_area_built - current_area_used
                ) * min_density

                # check if we can stock all the area built
                if current_seaweed_need > harvest_wet_with_loss:
                    new_area_used = current_seaweed_need / min_density
                    current_area_used += new_area_used
                    current_seaweed = seaweed_remaining_to_grow + harvest_wet_with_loss
                else:
                    harvest_for_food = harvest_wet_with_loss - current_seaweed_need
                    df.loc[current_day, "harvest_for_food"] = harvest_for_food
                    cumulative_harvest_for_food += harvest_for_food
                    new_area_used = current_seaweed_need / min_density
                    # calculate the new amount of current seaweed with the
                    # newly stocked area
                    current_area_used += new_area_used
                    current_seaweed = current_area_used * min_density

                df.loc[current_day, "new_area_used"] = new_area_used
            # Increment the harvest counter
            harvest_intervall += 1
            df.loc[current_day, "current_seaweed_need"] = current_seaweed_need
            df.loc[current_day, "current_area_built"] = current_area_built
            df.loc[current_day, "current_area_used"] = current_area_used
            df.loc[current_day, "current_seaweed"] = current_seaweed
            df.loc[current_day, "current_density"] = current_density
            df.loc[
                current_day, "cumulative_harvest_for_food"
            ] = cumulative_harvest_for_food
        return df

    def determine_average_productivity(
        self,
        growth_rate_fraction,
        days_to_run,
        percent_usable_for_growth,
        optimal_growth_rate,
    ):
        """
        Let the model run for one km² to determine the productivity
        per area and day and the harvest intervall
        Arguments:
            growth_rate_fraction: float or list of the growth rate of seaweed
            days_to_run: int, number of days to run the model
            percent_usable_for_growth: float, the percentage of the module area
                that can be used for growth
            optimal_growth_rate: float, the optimal growth rate of the seaweed
        Returns:
            productivity: float, the average productivity per km² and day
        """
        harvest_df = self.seaweed_growth(
            initial_seaweed=1,
            initial_area_built=1,
            initial_area_used=1,
            new_module_area_per_day=0,
            min_density=1200,
            max_density=3600,
            max_area=1,
            optimal_growth_rate=optimal_growth_rate,  # % per day
            growth_rate_fraction=growth_rate_fraction,
            initial_lag=0,
            percent_usable_for_growth=percent_usable_for_growth,
            days_to_run=days_to_run,
        )
        # Get the stabilized values
        try:
            stable_harvest_intervall = harvest_df.loc[
                harvest_df["harvest_intervall"].last_valid_index(), "harvest_intervall"
            ]
            stable_harvest_for_food = harvest_df.loc[
                harvest_df["harvest_for_food"].last_valid_index(), "harvest_for_food"
            ]
        except KeyError:
            stable_harvest_intervall = None
            stable_harvest_for_food = None
        print("stable_harvest_intervall", stable_harvest_intervall)
        print("stable_harvest_for_food", stable_harvest_for_food)
        # Calculate productivity per km² per day
        if stable_harvest_intervall is not None and stable_harvest_for_food is not None:
            productivity_day_km2 = stable_harvest_for_food / stable_harvest_intervall
        else:
            productivity_day_km2 = None
        print("productivity_day_km2", productivity_day_km2)
        return productivity_day_km2


def self_shading(density):
    """
    Calculates how much the growth rate is reduced due to self shading.
    Based on the publication:
    James, S.C. and Boriah, V. (2010), Modeling algae growth
    in an open-channel raceway
    Journal of Computational Biology, 17(7), 895−906.
    Arguments:
        density: the seaweed density
    Returns:
        the growth rate fraction
    """
    assert density > 0
    if density < 0.4:  # kg/m²
        return 1
    else:
        return math.exp(-0.513 * (density - 0.4))


def calculate_seaweed_need(
    global_pop,
    calories_per_person_per_day,
    food_waste,
    calories_per_t_seaweed_wet,
    iodine_limit,
):
    """
    Calculates the amount of seaweed needed to feed the population
    based on global population and the amount of seaweed needed per person
    limited by the iodine content of the seaweed
    Arguments:
        global_pop (int): Global population
        calories_per_person_per_day (int): Calories needed per person per day
        food_waste (float): Fraction of food wasted
        calories_per_kg_seaweed (int): Calories per t of seaweed
        iodine_limit (float): how large a fraction of the food can be substituted by seaweed
    Returns:
        float: amount of seaweed needed to feed the population
    """
    # Calculate the amount of calories needed to feed the population
    global_food_demand = global_pop * calories_per_person_per_day
    # Multiply by the fraction of food wasted
    global_food_demand = global_food_demand * ((1 + food_waste) / 100)
    # Multiply by the iodine limit, as we cannot have more than that
    global_food_demand = global_food_demand * iodine_limit
    # Calculate the amount of seaweed needed
    seaweed_needed = global_food_demand / calories_per_t_seaweed_wet
    return seaweed_needed


def seaweed_farm_area_per_day(day):
    """
    Estimates the area that can be built per day
    based on how many days have passed. This is a rough estimate
    based on:
        https://github.com/allfed/Seaweed-Scaleup-Model/blob/main/scripts/Logistic%20Growth.ipynb
    Arguments:
        day: the day
    Returns:
        the area that can be built per day
    """
    # The parameter values based on the fitting
    max_L = 4.15610385e03
    k = 2.83799528e-02
    x0 = 1.57630971e02
    off = -4.10270637e01
    # Calculate the area that can be built per day
    area_per_day = logistic_curve(day, max_L, k, x0, off)
    return area_per_day


def logistic_curve(x, max_L, k, x0, off):
    """
    Describes a logistic growth curve
    Arguments:
        x: value to calculate
        max_L: maximum value of the curve
        k: the logistic growth rate
        x0: the sigmoid's midpoint
        off: offset to 0
    Returns
        float: y value corresponding to x
    """
    return max_L / (1 + np.exp(-k * (x - x0))) + off


def run_model(
    optimal_growth_rate,
    days_to_run,
    global_pop,
    calories_per_person_per_day,
    harvest_loss,
    food_waste,
    calories_per_t_seaweed_wet,
    food_limit,
    feed_limit,
    biofuel_limit,
    percent_usable_for_growth,
    scenarios,
    location,
    number_of_clusters,
):
    """
    Run the model
    Arguments:
        optimal_growth_rate (float): the optimal growth rate
        days_to_run (int): the number of days to run the model
        global_pop (int): Global population
        calories_per_person_per_day (int): Calories needed per person per day
        harvest_loss (float): Fraction of harvest lost
        food_waste (float): Fraction of food wasted
        calories_per_kg_seaweed (int): Calories per t of seaweed
        food_limit (float): how large a fraction of the food can be substituted by seaweed
        feed_limit (float): how large a fraction of the feed can be substituted by seaweed
        biofuel_limit (float): how large a fraction of the biofuel can be substituted by seaweed
        percent_usable_for_growth (float): how much of the harvest is usable for growth
        scenarios (list): list of scenarios to run
        location (str): location on the globe
        number_of_clusters (int): number of clusters
    Returns:
        None
    """
    # Fraction of max calories we want in seaweed
    seaweed_limit = feed_limit + food_limit + biofuel_limit
    # Calculate the seaweed needed per day to feed everyone, given the iodine limit
    seaweed_needed = calculate_seaweed_need(
        global_pop,
        calories_per_person_per_day,
        food_waste,
        calories_per_t_seaweed_wet,
        seaweed_limit,
    )
    # Save the results for each scenario
    scenario_max_growth_rates = []
    # Run for all scenarios
    for scenario in scenarios:
        print("Running scenario {}".format(scenario))
        # Initialize the model
        for cluster in range(0, number_of_clusters):
            path = "data" + os.sep + location + os.sep + scenario
            model = SeaweedScaleUpModel(path, cluster, seaweed_needed, harvest_loss)
            growth_rate_fraction = np.mean(model.growth_timeseries)
            print(
                "Cluster {} has a median growth rate of {}".format(
                    cluster, growth_rate_fraction
                )
            )
            scenario_max_growth_rates.append((scenario, cluster, growth_rate_fraction))
            # calculate how much area we need to satisfy the daily
            # seaweed need with the given productivity
            productivity_day_km2 = model.determine_average_productivity(
                growth_rate_fraction,
                days_to_run,
                percent_usable_for_growth,
                optimal_growth_rate,
            )
            # check if the area is even productive enough to be used
            if productivity_day_km2 is not None:
                print("calculating yield for cluster {}".format(cluster))
                max_area = seaweed_needed / productivity_day_km2
                harvest_df = model.seaweed_growth(
                    initial_seaweed=10000,
                    initial_area_built=100,
                    initial_area_used=100,
                    new_module_area_per_day=100,
                    min_density=1200,
                    max_density=3600,
                    max_area=max_area,
                    optimal_growth_rate=optimal_growth_rate,
                    growth_rate_fraction=model.growth_timeseries,
                    initial_lag=0,  # 0 because this is taken care of with the logistic growth
                    percent_usable_for_growth=percent_usable_for_growth,
                    days_to_run=days_to_run,
                )
                harvest_df["max_area"] = max_area
                harvest_df["cluster"] = cluster
                harvest_df["seaweed_needed_per_day"] = seaweed_needed
                harvest_df.to_csv(
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
            else:
                print(
                    "Not enough productivity in cluster for production {}, skipping it".format(
                        cluster
                    )
                )
        print("done")
    # Convert the results to a dataframe
    scenario_max_growth_rates_df = pd.DataFrame(
        scenario_max_growth_rates, columns=["scenario", "cluster", "max_growth_rate"]
    )
    scenario_max_growth_rates_df.to_csv(
        "results" + os.sep + location + os.sep + "scenario_max_growth_rates.csv"
    )
