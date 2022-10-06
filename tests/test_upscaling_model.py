"""
Tests the upscaling model.
"""
import pytest

from src.upscaling_model import SeaweedUpscalingModel


def test_initialize_model():
    """
    Tests if the model can be initiliazed
    """
    model = SeaweedUpscalingModel(
        "data/constants.csv",
        initial_seaweed=1000,
        initial_area_built=1000,
        initial_area_used=1000,
        min_density=400,
        max_density=4000,
        initial_lag=0,
        max_area=1000000,
        additional_saturation_time=1.10,
    )

    assert model is not None
    # Test basic parameters
    assert model.parameters["initial_seaweed"] == 1000
    assert model.parameters["initial_area_built"] == 1000
    assert model.parameters["initial_area_used"] == 1000
    assert model.parameters["min_density"] == 400
    assert model.parameters["max_density"] == 4000
    assert model.parameters["initial_lag"] == 0
    assert model.parameters["max_area"] == 1000000
    assert model.parameters["additional_saturation_time"] == 1.10
    # Test constants
    assert model.parameters["calorie_demand"] == 2250


def test_parameter_calculation():
    """
    Tests if all the parameters were calculated correctly
    """
    model = SeaweedUpscalingModel("data/constants.csv")
    assert model.parameters["seedling_line_length"] == pytest.approx(5.19, 0.1)
    assert model.parameters["space_between_seedling_line"] == pytest.approx(0.781, 0.01)
    assert model.parameters["modules_per_area"] == pytest.approx(44.44, 0.1)
    assert model.parameters["longline_per_area"] == pytest.approx(666.66, 0.1)
    assert model.parameters["seedling_line_per_area"] == pytest.approx(128000, 0.1)
    assert model.parameters["buoys_per_area"] == pytest.approx(16666.66, 0.1)
    assert model.parameters["length_longline_per_area"] == pytest.approx(146.66, 0.1)
    assert model.parameters["weight_longline_per_area"] == pytest.approx(16.265, 0.01)
    assert model.parameters["weight_seedling_line_per_area"] == pytest.approx(
        16.63, 0.01
    )
    assert model.parameters["weight_rope_total_per_area"] == pytest.approx(32.89, 0.01)
    assert model.parameters[
        "upscale_needed_to_twist_all_synthethic_fiber"
    ] == pytest.approx(114, 0.01)
    assert model.parameters["new_module_area_per_day"] == pytest.approx(2134, 0.01)
    assert model.parameters["production_rate_per_longline_machine"] == pytest.approx(
        6.38, 0.1
    )
    assert model.parameters[
        "production_rate_per_seedling_line_machine"
    ] == pytest.approx(0.1810, 0.001)
    assert model.parameters["longline_machines_needed"] == pytest.approx(5442, 0.1)
    assert model.parameters["seedling_line_machines_needed"] == pytest.approx(
        196137.857, 0.1
    )
    assert model.parameters["total_cost_longline_machines"] == pytest.approx(
        50943693, 0.1
    )
    assert model.parameters["total_cost_seedling_line_machines"] == pytest.approx(
        1835843735.61, 0.1
    )
    assert model.parameters["total_cost_rope_machinery"] == pytest.approx(
        1886787429, 0.1
    )


def test_seaweed_growth():
    """
    Tests if the growth calculations finish correctly
    """
    model = SeaweedUpscalingModel("data/constants.csv")
    df = model.seaweed_growth(
        harvest_loss=model.parameters["harvest_loss"],
        initial_seaweed=model.parameters["initial_seaweed"],
        initial_area_built=model.parameters["initial_area_built"],
        initial_area_used=model.parameters["initial_area_used"],
        new_module_area_per_day=model.parameters["new_module_area_per_day"],
        min_density=model.parameters["min_density"],
        max_density=model.parameters["max_density"],
        max_area=model.parameters["max_area"],
        growth_rate=5,
        initial_lag=model.parameters["initial_lag"],
        percent_usable_for_growth=model.parameters["percent_usable_for_growth"],
        days_to_run=10,
    )
    assert df is not None
    assert df.shape == (10, 13)
    assert df["harvest_intervall"] is not None


def test_determine_productivity():
    """
    Tests if the productivity calculations finish correctly
    """
    model = SeaweedUpscalingModel("data/constants.csv")
    productivity_day_km2 = model.determine_productivity(
        growth_rate=5,
        harvest_loss=0.15,
        min_density=400,
        max_density=4000,
        percent_usable_for_growth=50,
        days_to_run=100,
    )

    assert productivity_day_km2 is not None
    assert productivity_day_km2 == 4080.0


def test_run_model_for_set_of_growth_rates():
    """
    Tests if the model runs correctly for a set of growth rates
    """
    model = SeaweedUpscalingModel("data/constants.csv")
    assert len(model.growth_rate_results) == 0
    model.run_model_for_set_of_growth_rates(
        growth_rates=[5, 10, 15, 25], days_to_run=365
    )
    assert len(model.growth_rate_results) != 0
    assert model.growth_rate_results["5"][0].shape == (365, 13)
    result_25_df = model.growth_rate_results["25"][0]
    assert result_25_df.loc[
        result_25_df.index[-1], "cumulative_harvest_for_food"
    ] == pytest.approx(243461131503, 0.1)
