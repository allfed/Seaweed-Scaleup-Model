"""
Model to calculate the time it takes to upscale global seaweed production
"""
import pandas as pd
import matplotlib.pyplot as plt


class SeaweedUpscalingModel:
    """
    Class that loads the data, calculates the upscaling and plots it
    """

    def __init__(
        self,
        path,
        initial_seaweed=1000,
        initial_area_built=1000,
        initial_area_used=1000,
        min_density=400,
        max_density=4000,
        initial_lag=0,
        max_area=1000000,
        additional_saturation_time=1.10,
        calories_from_seaweed=20,
    ):
        """
        Initialize the model
        """
        self.model_data_calculated = False
        self.parameters = {}
        self.growth_rate_results = {}
        self.labor_results = {}
        self.parameters["calories_from_seaweed"] = calories_from_seaweed
        self.load_literature_parameters(path)
        self.calculate_basic_parameters()
        # Set model starting values
        self.parameters["initial_seaweed"] = initial_seaweed  # t
        self.parameters[
            "initial_area_built"
        ] = initial_area_built  # km2 that are already prepared for seaweed production
        self.parameters[
            "initial_area_used"
        ] = initial_area_used  # km2 that are already used for seaweed production
        # Min and max density based on James, S.C. and Boriah, V. (2010),
        self.parameters["min_density"] = min_density  # minmal seaweed density t/km2
        self.parameters["max_density"] = max_density  # t/km2
        self.parameters[
            "max_area"
        ] = max_area  # maximal area that is to be used for seaweed production km2
        self.parameters[
            "initial_lag"
        ] = initial_lag  # days until production starts (meant to model how long it takes people
        # to get their act together after a nuclear war)
        self.parameters[
            "additional_saturation_time"
        ] = additional_saturation_time  # To accomodate for lost plants we assume 10 percent
        # more time spent at harvest for resaturation
        # also the plants have to be renewed at least every three years.

    def load_literature_parameters(self, path):
        """
        Load the parameters we found resonable values for from the file
        """
        constants_temp = pd.read_csv(path)
        for index in constants_temp.index:
            self.parameters[constants_temp.loc[index, "variable"]] = constants_temp.loc[
                index, "value"
            ]

    def calculate_basic_parameters(self):
        """
        Calls all the other functinos for basic parametesr
        """
        self.calculate_global_food_demand_parameters()
        self.calculate_seaweed_farm_design_parameters()
        self.calculate_seaweed_farm_design_per_km2_parameters()
        self.calculate_synthetic_fiber_parameters()
        self.calculate_scaling_parameters()
        self.calculate_rope_parameters()

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

    def calculate_seaweed_farm_design_parameters(self):
        """
        Calculates the parameters needed to built a seaweed farm
        """
        self.parameters["seedling_line_length"] = (
            self.parameters["seedling_line_length_per_longline"]
            / self.parameters["seedling_line_per_longline"]
        )  #
        self.parameters["space_between_seedling_line"] = (
            self.parameters["length_of_module"]
            / self.parameters["seedling_line_per_longline"]
        )

    def calculate_seaweed_farm_design_per_km2_parameters(self):
        """
        Calculates the material needed to construct a seaweed farm per km2
        """
        self.parameters["modules_per_area"] = 1000000 / (
            self.parameters["length_of_module"] * self.parameters["width_of_module"]
        )  # [1/km²]
        self.parameters["longline_per_area"] = (
            self.parameters["longline_per_module"] * self.parameters["modules_per_area"]
        )  # [1/km²]
        self.parameters["seedling_line_per_area"] = (
            self.parameters["modules_per_area"]
            * self.parameters["longline_per_module"]
            * self.parameters["seedling_line_per_longline"]
        )  # [1/km²]
        self.parameters["buoys_per_area"] = (
            self.parameters["modules_per_area"]
            * self.parameters["longline_per_module"]
            * self.parameters["buoys_per_longline"]
        )  # [1/km²]
        self.parameters["length_longline_per_area"] = (
            self.parameters["longline_per_area"] * self.parameters["longline_length"]
        ) / 1000  # [km/km²]
        self.parameters["length_seedling_line_per_area"] = (
            self.parameters["seedling_line_per_area"]
            * self.parameters["seedling_line_length"]
        ) / 1000  # [km/km²]
        self.parameters["weight_longline_per_area"] = (
            self.parameters["length_longline_per_area"]
            * self.parameters["longline_density"]
        )  # [T/km²]
        self.parameters["weight_seedling_line_per_area"] = (
            self.parameters["length_seedling_line_per_area"]
            * self.parameters["seedling_line_density"]
        )  # [T/km²]
        self.parameters["weight_rope_total_per_area"] = (
            self.parameters["weight_longline_per_area"]
            + self.parameters["weight_seedling_line_per_area"]
        )  # [T/km²]

    def calculate_synthetic_fiber_parameters(self):
        """
        Calculates the synthetic fiber parameters
        """
        self.parameters["synthethic_fiber_production_global_day"] = (
            self.parameters["synthethic_fiber_production_global_useful"] / 365
        )  # [T/day]

    def calculate_scaling_parameters(self):
        """
        Calculates the parameters needed for scaling up the farms
        """
        self.parameters["new_module_area_per_day"] = (
            self.parameters["synthethic_fiber_production_global_day"]
            / self.parameters["weight_rope_total_per_area"]
        )  # [km²/day]

    def calculate_rope_parameters(self):
        """
        Calculates the parameters for the rope machinery
        """
        self.parameters["production_rate_per_longline_machine"] = (
            2502 / 1000 * (24 / 8) * self.parameters["runtime"] / 100
        )  # [T/day]
        self.parameters["production_rate_per_seedling_line_machine"] = (
            71 / 1000 * (24 / 8) * self.parameters["runtime"] / 100
        )  # [T/day]
        self.parameters["production_day"] = (
            self.parameters["production_year"] / 365
        )  # [T/day]
        self.parameters["upscale_needed_to_twist_all_synthethic_fiber"] = (
            self.parameters["synthethic_fiber_production_global_day"]
            / self.parameters["production_day"]
        )  # [ ]
        self.parameters["longline_machines_needed"] = self.parameters[
            "new_module_area_per_day"
        ] * (
            self.parameters["weight_longline_per_area"]
            / self.parameters["production_rate_per_longline_machine"]
        )  # [ ]
        self.parameters["seedling_line_machines_needed"] = (
            self.parameters["new_module_area_per_day"]
            * self.parameters["weight_seedling_line_per_area"]
            / self.parameters["production_rate_per_seedling_line_machine"]
        )  # [ ]
        self.parameters["total_cost_longline_machines"] = (
            self.parameters["cost_per_longline_machine"]
            * self.parameters["longline_machines_needed"]
            * (1 + (self.parameters["increased_cost_due_to_rapid_tooling"] / 100))
        )  # [$]
        self.parameters["total_cost_seedling_line_machines"] = (
            self.parameters["cost_per_seedling_line_machine"]
            * self.parameters["seedling_line_machines_needed"]
            * (1 + (self.parameters["increased_cost_due_to_rapid_tooling"] / 100))
        )  # [$]
        self.parameters["total_cost_rope_machinery"] = (
            self.parameters["total_cost_longline_machines"]
            + self.parameters["total_cost_seedling_line_machines"]
        )  # [$]

    def seaweed_growth(
        self,
        harvest_loss,
        initial_seaweed,
        initial_area_built,
        initial_area_used,
        new_module_area_per_day,
        min_density,
        max_density,
        max_area,
        growth_rate,
        initial_lag,
        percent_usable_for_growth,
        days_to_run,
    ):
        """
        Calculates the seaweed growth and creatss a dataframe of all important
        growth numbers
        """
        # Initialize
        current_area_built = initial_area_built
        current_area_used = initial_area_used
        current_seaweed = initial_seaweed
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
            # Let the seaweed grow
            current_seaweed = current_seaweed * growth_rate
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

    def determine_productivity(
        self,
        growth_rate,
        harvest_loss,
        min_density,
        max_density,
        percent_usable_for_growth,
        days_to_run,
    ):
        """
        Let the model run for one km² to determine the productivity 
        per area and day and the harvest intervall
        """
        df = self.seaweed_growth(
            harvest_loss=harvest_loss,
            initial_seaweed=1,
            initial_area_built=1,
            initial_area_used=1,
            new_module_area_per_day=0,
            min_density=min_density,
            max_density=max_density,
            max_area=1,
            growth_rate=growth_rate,
            initial_lag=0,
            percent_usable_for_growth=percent_usable_for_growth,
            days_to_run=days_to_run,
        )
        # Get the stabilized values
        assert df["harvest_intervall"] is not None
        stable_harvest_intervall = df.loc[
            df["harvest_intervall"].last_valid_index(), "harvest_intervall"
        ]
        stable_harvest_for_food = df.loc[
            df["harvest_for_food"].last_valid_index(), "harvest_for_food"
        ]

        print("stable_harvest_intervall", stable_harvest_intervall)
        print("stable_harvest_for_food", stable_harvest_for_food)
        # Calculate productivity per km² per day
        productivity_day_km2 = stable_harvest_for_food / stable_harvest_intervall
        print("productivity_day_km2", productivity_day_km2)
        return productivity_day_km2

    def run_model_for_set_of_growth_rates(
        self, growth_rates=[5, 10, 15, 25], days_to_run=365
    ):
        """
        Runs the model for a bunch of growth rates (in %) and returns the results
        as a dictionary of dataframes
        """
        for growth_rate in growth_rates:
            # convert to fraction
            growth_rate_frac = (100 + growth_rate) / 100
            # determine productivity in t per day per km²
            print("\nRun model for 1 km² with growth rate :" + str(growth_rate) + " %")
            productivity_day_km2 = self.determine_productivity(
                growth_rate_frac,
                self.parameters["harvest_loss"],
                self.parameters["min_density"],
                self.parameters["max_density"],
                self.parameters["percent_usable_for_growth"],
                days_to_run,
            )
            # calculate how much area we need to satisfy the daily seaweed need 
            # with the given productivity
            max_area = self.parameters["seaweed_needed"] / productivity_day_km2
            print("max_area", max_area)
            # run the actual model
            print("\nRun full model with growth rate :" + str(growth_rate) + " %")
            df = self.seaweed_growth(
                harvest_loss=self.parameters["harvest_loss"],
                initial_seaweed=self.parameters["initial_seaweed"],
                initial_area_built=self.parameters["initial_area_built"],
                initial_area_used=self.parameters["initial_area_used"],
                new_module_area_per_day=self.parameters["new_module_area_per_day"],
                min_density=self.parameters["min_density"],
                max_density=self.parameters["max_density"],
                max_area=max_area,
                growth_rate=growth_rate_frac,
                initial_lag=self.parameters["initial_lag"],
                percent_usable_for_growth=self.parameters["percent_usable_for_growth"],
                days_to_run=days_to_run,
            )
            # Save results
            self.growth_rate_results[str(growth_rate)] = (df, max_area)

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


if __name__ == "__main__":
    model = SeaweedUpscalingModel("data/constants.csv")
    model.run_model_for_set_of_growth_rates(growth_rates=[4, 8, 12], days_to_run=400)
    model.plot_satisfaction_results()
    model.plot_area_results()
