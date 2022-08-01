"""
Model to calculate the time it takes to upscale global seaweed production
"""
import pandas as pd


class SeaweedUpscalingModel:
    """
    Class that loads the data, calculates the upscaling and plots it
    """
    def __init__(self, path, initial_seaweed=1000,
                 initial_area_built=1000, initial_area_used=1000,
                 min_density=400, max_density=4000,
                 initial_lag=0, max_area=1000000,
                 additional_saturation_time=1.10):
        """
        Initialize the model
        """
        self.parameters= {}
        self.load_literature_parameters(path)
        self.calculate_basic_parameters()
        # Set model starting values
        self.initial_seaweed=initial_seaweed # t
        self.initial_area_built=initial_area_built # km2 that are already prepared for seaweed production
        self.initial_area_used=initial_area_used # km2 that are already used for seaweed production
        # Min and max density based on James, S.C. and Boriah, V. (2010), 
        self.min_density=min_density # minmal seaweed density t/km2
        self.max_density=max_density # t/km2
        self.max_area=max_area # maximal area that is to be used for seaweed production km2
        self.initial_lag=initial_lag # days until production starts (meant to model how long it takes people 
        # to get their act together after a nuclear war)
        self.additional_saturation_time=additional_saturation_time # To accomodate for lost plants we assume 10 percent 
        # more time spent at harvest for resaturation
        # also the plants have to be renewed at least every three years. 


    def load_literature_parameters(self, path):
        """
        Load the parameters we found resonable values for from the file
        """
        constants_temp = pd.read_csv(path)
        for index in constants_temp.index:
            self.parameters[constants_temp.loc[index, "variable"]] = constants_temp.loc[index, "value"]      


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
            self.parameters["calorie_demand"] * self.parameters["population"] * 
            (1 + self.parameters["food_waste_in_catastrophe"] / 100))
        

    def calculate_seaweed_farm_design_parameters(self):
        """
        Calculates the parameters needed to built a seaweed farm
        """
        self.parameters["seedling_line_length"] = (
                    self.parameters["seedling_line_length_per_longline"] / self.parameters["seedling_line_per_longline"] ) #	
        self.parameters["space_between_seedling_line"] = (
                    self.parameters["length_of_module"] / self.parameters["seedling_line_per_longline"])


    def calculate_seaweed_farm_design_per_km2_parameters(self):
        """
        Calculates the material needed to construct a seaweed farm per km2
        """
        self.parameters["modules_per_area"] = 1000000 / (self.parameters["length_of_module"] * self.parameters["width_of_module"]) # [1/km²]
        self.parameters["longline_per_area"] = self.parameters["longline_per_module"] * self.parameters["modules_per_area"] # [1/km²]
        self.parameters["seedling_line_per_area"] = (self.parameters["modules_per_area"] * 
                                                    self.parameters["longline_per_module"] * self.parameters["seedling_line_per_longline"]) #[1/km²]
        self.parameters["buoys_per_area"] = self.parameters["modules_per_area"] * self.parameters["longline_per_module"] * self.parameters["buoys_per_longline"] # [1/km²]
        self.parameters["length_longline_per_area"] = (self.parameters["longline_per_area"] * 
                                                        self.parameters["longline_length"]) / 1000 # [km/km²]
        self.parameters["length_seedling_line_per_area"] = (self.parameters["seedling_line_per_area"] *
                                                         self.parameters["seedling_line_length"])/1000 # [km/km²]
        self.parameters["weight_longline_per_area"] = self.parameters["length_longline_per_area"] * self.parameters["longline_density"] # [T/km²]
        self.parameters["weight_seedling_line_per_area"] = self.parameters["length_seedling_line_per_area"] * self.parameters["seedling_line_density"] #[T/km²]
        self.parameters["weight_rope_total_per_area"] = self.parameters["weight_longline_per_area"] + self.parameters["weight_seedling_line_per_area"] # [T/km²]


    def calculate_synthetic_fiber_parameters(self):
        """
        Calculates the synthetic fiber parameters
        """
        self.parameters["synthethic_fiber_production_global_day"] = self.parameters["synthethic_fiber_production_global_useful"] / 365 # [T/day]
    
    def calculate_scaling_parameters(self):
        """
        Calculates the parameters needed for scaling up the farms
        """
        self.parameters["new_module_area_per_day"] = self.parameters["synthethic_fiber_production_global_day"] / self.parameters["weight_rope_total_per_area"] # [km²/day]	

    
    def calculate_rope_parameters(self):
        """
        Calculates the parameters for the rope machinery
        """
        self.parameters["production_rate_per_longline_machine"] = 2502/1000*(24/8)*self.parameters["runtime"]/100	# [T/day]
        self.parameters["production_rate_per_seedling_line_machine"] = 71/1000*(24/8)*self.parameters["runtime"]/100 # [T/day]
        self.parameters["production_day"] = self.parameters["production_year"]/365 # [T/day]	
        self.parameters["upscale_needed_to_twist_all_synthethic_fiber"] = self.parameters["synthethic_fiber_production_global_day"] / self.parameters["production_day"]	#	[ ]	
        self.parameters["longline_machines_needed"] = self.parameters["new_module_area_per_day"] * (self.parameters["weight_longline_per_area"]/self.parameters["production_rate_per_longline_machine"]) # [ ] 
        self.parameters["seedling_line_machines_needed"] = self.parameters["new_module_area_per_day"] * self.parameters["weight_seedling_line_per_area"]/self.parameters["production_rate_per_seedling_line_machine"] # [ ]	
        self.parameters["total_cost_longline_machines"] = self.parameters["cost_per_longline_machine"] * self.parameters["longline_machines_needed"] * (1+(self.parameters["increased_cost_due_to_rapid_tooling"]/100))	# [$]	
        self.parameters["total_cost_seedling_line_machines"] = self.parameters["cost_per_seedling_line_machine"] * self.parameters["seedling_line_machines_needed"] * (1+(self.parameters["increased_cost_due_to_rapid_tooling"]/100)) # [$]	
        self.parameters["total_cost_rope_machinery"] = self.parameters["total_cost_longline_machines"] + self.parameters["total_cost_seedling_line_machines"] # [$]	


    