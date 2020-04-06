# selected individual trips for quality measurement calculation tests
import pytest
from tripmining.model.traveler import Traveler

from test.qualitymeasurements.utils import load_trip, prepare_traveler_from_raw_data, imitate_trip_id

selected_individual_trips = ["trip1", "trip2", "trip3", "trip4"]

# loading the selected strip from files
trips = [load_trip(trip) for trip in selected_individual_trips]

# prepare the checkin history of the traveler
traveler_checkins = prepare_traveler_from_raw_data(trips)

# generating the trip id imitating the trip id generation of the library
trip_name_id_map = {trip["name"]: imitate_trip_id(trip) for trip in trips}

# data preparation for the parameterized test
'''
parameterized    data structure
[]
'''
filter_test_combinations = [(7, 0.2, 1, 50000, 1, ["trip1", "trip2", "trip3", "trip4"], traveler_checkins)]

@pytest.mark.parametrize('min_duration, min_density, max_inter_streak_days, max_speed, max_checkin_discontinuity, '
                         'expected_trips, traveler_checkins', filter_test_combinations)
def test_all_filters(min_duration, min_density, max_inter_streak_days, max_speed, max_checkin_discontinuity,
                     expected_trips, traveler_checkins):
    generated_trips = Traveler.from_checkins(traveler_checkins,
                                             'twitter',
                                             min_duration=min_duration,
                                             min_density=min_density,
                                             max_inter_streak_days=max_inter_streak_days,
                                             max_speed=max_speed,
                                             max_checkin_discontinuity=max_checkin_discontinuity).trips
    assert set([trip_name_id_map[exp] for exp in expected_trips]) == set([trip.trip_id for trip in generated_trips])