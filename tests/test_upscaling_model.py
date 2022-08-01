"""
Tests the upscaling model.
"""
from src.upscaling_model import SeaweedUpscalingModel


def test_initialize_model():
    """
    Tests if the model can be initiliazed
    """
    model = SeaweedUpscalingModel("data/constants.csv", initial_seaweed=1000,
                    initial_area_built=1000, initial_area_used=1000,
                    min_density=400, max_density=4000,
                    initial_lag=0, max_area=1000000,
                    additional_saturation_time=1.10)
    assert model is not None    
    # Test basic parameters
    assert model.initial_seaweed == 1000
    assert model.initial_area_built == 1000
    assert model.initial_area_used == 1000
    assert model.min_density == 400
    assert model.max_density == 4000
    assert model.initial_lag == 0
    assert model.max_area == 1000000
    assert model.additional_saturation_time == 1.10
    # Test constants
    assert model.parameters["calorie_demand"] == 2200


def test_parameter_calculation():
    """
    Tests if all the parameters were calculated correctly
    """
    model = SeaweedUpscalingModel("data/constants.csv")
    assert model.parameters["seedling_line_length"] == 5.197916666666667
    assert model.parameters["space_between_seedling_line"] == 0.78125
    assert model.parameters["modules_per_area"] == 44.44444444444444
    assert model.parameters["longline_per_area"] == 666.6666666666666
    assert model.parameters["seedling_line_per_area"] == 128000.0
    assert model.parameters["buoys_per_area"] == 16666.666666666664
    assert model.parameters["length_longline_per_area"] == 146.66666666666666
    assert model.parameters["weight_longline_per_area"] == 16.26533333333333
    assert model.parameters["weight_seedling_line_per_area"] == 16.633333333333336
    assert model.parameters["weight_rope_total_per_area"] == 32.89866666666667
