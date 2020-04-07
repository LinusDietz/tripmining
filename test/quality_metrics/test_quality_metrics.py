import pytest
from tripmining.model.traveler import Traveler
from test.quality_metrics.utils import prepare_chekins_from_raw_data, load_trip

# selected individual trips for quality measurement calculation tests
selected_trips = ["trip1", "trip2", "trip3", "trip4"]

# loading the selected strip from files
trips = [load_trip(trip) for trip in selected_trips]


@pytest.mark.parametrize('trip', trips)
def test_checkin_density(trip):
    """
    Test for the checkin density value calculation
    :param trip: loaded trip information
    """
    extracted_trip = round(
        Traveler.from_checkins(prepare_chekins_from_raw_data(trip), 'twitter').trips.pop().to_dict()[
            "checkin_density"], 4)
    expected_checkin_density = trip["attributes"]["checkin_density"]
    assert extracted_trip == expected_checkin_density, "Expected Checkin Density is different"


@pytest.mark.parametrize('trip', trips)
def test_inter_streak_days(trip):
    """
    Test for the inter streak days value calculation
    :param trip: loaded trip information
    """
    extracted_inter_streak_days = round(
        Traveler.from_checkins(prepare_chekins_from_raw_data(trip), 'twitter').trips.pop().to_dict()[
            "inter_streak_days"], 4)
    expected_inter_streak_days = trip["attributes"]["inter_streak_days"]
    assert extracted_inter_streak_days == expected_inter_streak_days, "Expected Inter Streak Days is different"


@pytest.mark.parametrize('trip', trips)
def test_checkin_discontinuity(trip):
    """
    Test for the checkin discontinuity value calculation
    :param trip: loaded trip information
    """
    extracted_checkin_discontinuity = round(
        Traveler.from_checkins(prepare_chekins_from_raw_data(trip), 'twitter').trips.pop().to_dict()[
            "checkin_discontinuity"], 4)
    expected_checkin_discontinuity = trip["attributes"]["checkin_discontinuity"]
    assert extracted_checkin_discontinuity == expected_checkin_discontinuity, \
        "Expected Checkin discontinuity is different"


@pytest.mark.parametrize('trip', trips)
def test_max_speed(trip):
    """
    Test for the max speed value calculation
    :param trip: loaded trip information
    """
    extracted_max_speed = round(
        Traveler.from_checkins(prepare_chekins_from_raw_data(trip), 'twitter').trips.pop().to_dict()[
            "max_transition_speed"], 0)
    expected_max_speed = trip["attributes"]["max_transition_speed"]
    assert extracted_max_speed == expected_max_speed, "Expected Max speed is different"
