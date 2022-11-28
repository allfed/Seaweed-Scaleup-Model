"""
Tests the upscaling model.
"""
import pandas as pd
import pytest

from src.scaleup_model import SeaweedScaleUpModel, self_shading


def test_initialize_model():
    """
    Tests if the model can be initiliazed
    """
    model = SeaweedScaleUpModel("data", 2, 1000, 20)
    assert model is not None
    assert model.seaweed_need == 1000
    assert model.harvest_loss == 20


def test_self_shading():
    """
    Tests if the self shading calculations finish correctly
    """
    model = SeaweedScaleUpModel("data", 2, 1000, 20)
    with pytest.raises(AssertionError):
        assert self_shading(0) == 0
    assert self_shading(0.1) == 1
    assert self_shading(5) == pytest.approx(0.094, 0.01)


def test_seaweed_growth():
    """
    Tests if the growth calculations finish correctly
    """
    seaweed_needed = 1000
    productivity_day_km2 = 4
    model = SeaweedScaleUpModel("data", 2, 1000, 20)
    max_area = seaweed_needed / productivity_day_km2
    harvest_df = model.seaweed_growth(
        initial_seaweed=10000,
        initial_area_built=100,
        initial_area_used=100,
        new_module_area_per_day=100,
        min_density=1000,
        max_density=4000,
        max_area=max_area,
        optimal_growth_rate=60,
        growth_rate_fraction=model.growth_timeseries,
        initial_lag=30,
        percent_usable_for_growth=50,
        days_to_run=100,
    )
    assert isinstance(harvest_df, pd.DataFrame)


def test_determine_productivity():
    """
    Tests if the productivity calculations finish correctly
    """
    model = SeaweedScaleUpModel("data", 2, 1000, 20)
    productivity_day_km2 = model.determine_average_productivity(
        growth_rate_fraction=0.5,
        days_to_run=100,
        percent_usable_for_growth=50
    )

    assert productivity_day_km2 is not None
    assert productivity_day_km2 == pytest.approx(178.5, 0.1)
