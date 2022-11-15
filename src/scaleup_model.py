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
    def __init__(
        self,
        path,
        cluster,
        seaweed_need,
        harvest_loss
    ):
        """
        Initialize the model
        """
        self.model_data_calculated = False
        self.parameters = {}
        self.optimal_growth_rate_results = {}
        self.seaweed_need = seaweed_need
        self.harvest_loss = harvest_loss
        self.load_growth_timeseries(path, cluster)

    def load_growth_timeseries(self, path, cluster):
        """
        Loads the growth timeseries from the file
        """
        growth_timeseries = pd.read_csv(
            path + os.sep + "actual_growth_rate_by_cluster.csv"
        )
        self.growth_timeseries = growth_timeseries["growth_daily_cluster_" + str(cluster)].to_list()

    def self_shading(self, density):
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
        if density < 0.4:  # kg/m²
            return 1
        else:
            return math.exp(-0.513 * (density - 0.4))

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
        verbose=False
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
        # We can only use a fraction of the module area to grow seaweed
        growth_area_per_day = new_module_area_per_day * (
            percent_usable_for_growth / 100
        )
        cumulative_harvest_for_food = 0
        current_seaweed_need = 0
        harvest_intervall = 0
        # collect all the harvest_intervall values to find the most common at the end
        harvest_intervall_all = []
        df = pd.DataFrame(index=range(days_to_run))
        for current_day in range(days_to_run):
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
            self_shading_factor = self.self_shading(
                current_density / 1000)  # convert to kg/m² from t/km2
            # Let the seaweed grow
            # This can be done with a fixed value for the growth rate fraction
            # or with a timeseries of the growth rate fraction
            if isinstance(growth_rate_fraction, float):
                actual_growth_rate = 1 + (
                    (optimal_growth_rate * growth_rate_fraction * self_shading_factor) / 100)
            elif isinstance(growth_rate_fraction, list):
                actual_growth_rate = 1 + (
                    (optimal_growth_rate * growth_rate_fraction[current_day] * self_shading_factor) / 100)
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
        percent_usable_for_growth
    ):
        """
        Let the model run for one km² to determine the productivity
        per area and day and the harvest intervall
        """
        harvest_df = self.seaweed_growth(
            initial_seaweed=1,
            initial_area_built=1,
            initial_area_used=1,
            new_module_area_per_day=0,
            min_density=1000,
            max_density=4000,
            max_area=1,
            optimal_growth_rate=60,  # % per day
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


def calculate_seaweed_need(
    global_pop,
    calories_per_person_per_day,
    food_waste,
    calories_per_t_seaweed_wet,
    iodine_limit
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


def run_model():
    days_to_run = 3600  # 120 month at 30 days per month
    global_pop = 7000000000
    calories_per_person_per_day = 2250
    harvest_loss = 20
    food_waste = 13  # https://www.researchsquare.com/article/rs-1446444/v1
    calories_per_t_seaweed_wet = 400000
    iodine_limit = 0.2  # https://academic.oup.com/jcem/article/87/12/5499/2823602
    # percent of the area of the module that can acutally be used for food production.
    # Rest is needed for things like lanes for harvesting
    percent_usable_for_growth = 50
    # Calculate the seaweed needed per day to feed everyone, given the iodine limit
    seaweed_needed = calculate_seaweed_need(
        global_pop,
        calories_per_person_per_day,
        food_waste,
        calories_per_t_seaweed_wet,
        iodine_limit
    )
    # Initialize the model
    for cluster in range(0, 4):
        model = SeaweedUpscalingModel("data", cluster, seaweed_needed, harvest_loss)
        growth_rate_fraction = np.mean(model.growth_timeseries)
        print("Cluster {} has a median growth rate of {}".format(cluster, growth_rate_fraction))
        # calculate how much area we need to satisfy the daily
        # seaweed need with the given productivity
        productivity_day_km2 = model.determine_average_productivity(
            growth_rate_fraction, days_to_run, percent_usable_for_growth)
        # check if the area is even productive enough to be used
        if productivity_day_km2 is not None:
            print("calculating yield for cluster {}".format(cluster))
            max_area = seaweed_needed / productivity_day_km2
            harvest_df = model.seaweed_growth(
                initial_seaweed=100,
                initial_area_built=100,
                initial_area_used=100,
                new_module_area_per_day=100,
                min_density=1000,
                max_density=4000,
                max_area=max_area,
                optimal_growth_rate=60,
                growth_rate_fraction=model.growth_timeseries,
                initial_lag=0,
                percent_usable_for_growth=percent_usable_for_growth,
                days_to_run=days_to_run)
            harvest_df["max_area"] = max_area
            harvest_df["cluster"] = cluster
            harvest_df["seaweed_needed_per_day"] = seaweed_needed
            harvest_df.to_csv(
                f"results/harvest_df_cluster_{cluster}.csv"
            )
        else:
            print("Not enough productivity in cluster for production {}, skipping it".format(
                cluster))
    print("done")


if __name__ == "__main__":
    run_model()
