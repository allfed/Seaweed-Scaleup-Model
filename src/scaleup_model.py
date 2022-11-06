"""
Model to calculate the time it takes to scaleup global seaweed production
"""
import pandas as pd
import numpy as np
import os
import math


class SeaweedUpscalingModel:
    """
    Class that loads the data, calculates the scaleup and saves it into a csv
    """
    def __init__(
        self,
        path,
        cluster,
        calories_from_seaweed=20,
    ):
        """
        Initialize the model
        """
        self.model_data_calculated = False
        self.parameters = {}
        self.optimal_growth_rate_results = {}
        self.parameters["calories_from_seaweed"] = calories_from_seaweed
        self.load_literature_parameters(path)
        self.load_growth_timeseries(path, cluster)
        self.calculate_global_food_demand_parameters()

    def load_literature_parameters(self, path):
        """
        Load the parameters we found resonable values for from the file
        """
        constants_temp = pd.read_csv(path + os.sep + "constants.csv")
        for parameter in constants_temp.index:
            value = constants_temp.loc[parameter, "value"]
            try:
                self.parameters[constants_temp.loc[parameter, "variable"]] = float(value)
            except ValueError:
                self.parameters[constants_temp.loc[parameter, "variable"]] = np.nan

    def load_growth_timeseries(self, path, cluster):
        """
        Loads the growth timeseries from the file
        """
        growth_timeseries = pd.read_csv(
            path + os.sep + "actual_growth_rate_by_cluster.csv"
        )
        self.growth_timeseries = growth_timeseries["growth_daily_cluster_" + str(cluster)].to_list()

    def calculate_global_food_demand_parameters(self):
        """
        Calculates the global demand for food
        """
        self.parameters["global_food_demand_in_catastrophe"] = (
            self.parameters["calorie_demand"]
            * self.parameters["population"]
            * (1 + self.parameters["food_waste_in_catastrophe"] / 100)
        )
        self.parameters["daily_calories_needed"] = self.parameters[
            "global_food_demand_in_catastrophe"
        ] * (self.parameters["calories_from_seaweed"] / 100)
        self.parameters["seaweed_needed"] = (
            self.parameters["daily_calories_needed"]
            / self.parameters["calories_per_wet_weight"]
        )  # [T/day]

    def self_shading(self, density):
        """
        Calculates how much the growth rate is reduced due to self shading.
        Based on the publication:
        James, S.C. and Boriah, V. (2010), Modeling algae growth
        in an open-channel raceway
        Journal of Computational Biology, 17(7), 895−906.
        args:
            density: the seaweed density
        returns:
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
    ):
        """
        Calculates the seaweed growth and creatss a dataframe of all important
        growth numbers
        Arguments:
            initial_seaweed: The initial amount of seaweed
            initial_area_built: The initial area built
            initial_area_used: The initial area used
            new_module_area_per_day: The area built per day
            min_density: The minimum density
            max_density: The maximum density
            max_area: The maximum area
            optimal_growth_rate: The optimal growth rate
            growth_rate_fraction: The fraction of the growth rate (can either be scalar or list)
            initial_lag: The initial lag
            percent_usable_for_growth: The percent usable for growth
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
            self_shading_factor = self.self_shading(current_density / 1000) # convert to kg/m² from t/km2
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
                print("harvest_wet", harvest_wet)
                # calculate harvest loss
                # make it a fraction
                harvest_loss = self.parameters["harvest_loss"] / 100
                assert harvest_loss <= 1 and harvest_loss >= 0
                harvest_wet_with_loss = harvest_wet * (1 - harvest_loss)
                df.loc[current_day, "harvest_wet_with_loss"] = harvest_wet_with_loss
                # calculate how much seaweed we would need to stock all aready built area
                current_seaweed_need = (
                    current_area_built - current_area_used
                ) * min_density

                # check if we can stock all the area built
                if current_seaweed_need > harvest_wet_with_loss:
                    new_area_used = harvest_wet_with_loss / min_density
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
            percent_usable_for_growth=self.parameters["percent_usable_for_growth"],
            days_to_run=days_to_run,
        )
        # Get the stabilized values
        assert harvest_df["harvest_intervall"] is not None
        stable_harvest_intervall = harvest_df.loc[
            harvest_df["harvest_intervall"].last_valid_index(), "harvest_intervall"
        ]
        stable_harvest_for_food = harvest_df.loc[
            harvest_df["harvest_for_food"].last_valid_index(), "harvest_for_food"
        ]
        print("stable_harvest_intervall", stable_harvest_intervall)
        print("stable_harvest_for_food", stable_harvest_for_food)
        # Calculate productivity per km² per day
        productivity_day_km2 = stable_harvest_for_food / stable_harvest_intervall
        print("productivity_day_km2", productivity_day_km2)
        return productivity_day_km2


def run_model():
    days_to_run = 500
    # Initialize the model
    for cluster in range(0, 5):
        model = SeaweedUpscalingModel("data", cluster)
        # TODO calculate this based on the cluster
        # does not make sense to to this as a forever single value
        productivity_day_km2 = model.determine_average_productivity(0.15, days_to_run)
        # calculate how much area we need to satisfy the daily
        # seaweed need with the given productivity
        max_area = model.parameters["seaweed_needed"] / productivity_day_km2
        harvest_df = model.seaweed_growth(
            initial_seaweed=1,
            initial_area_built=1,
            initial_area_used=1,
            new_module_area_per_day=1000,
            min_density=1000,
            max_density=4000,
            max_area=max_area,
            optimal_growth_rate=60,
            growth_rate_fraction=model.growth_timeseries,
            initial_lag=0,
            percent_usable_for_growth=model.parameters["percent_usable_for_growth"],
            days_to_run=days_to_run)
        harvest_df.to_csv(
            f"results/harvest_df_cluster_{cluster}.csv"
        )
    # Run the model
    print("done")


if __name__ == "__main__":
    run_model()
