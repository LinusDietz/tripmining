# selected individual trips for quality measurement calculation tests
import pytest
from tripmining.model.traveler import Traveler

from test.quality_metrics.utils import load_trip, prepare_traveler_from_raw_data, imitate_trip_id

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
[( min_duration, 
   min_density, 
   max_inter_streak_days, 
   max_speed, 
   max_checkin_discontinuity,
   expected_trips
   traveler_checkins']
'''
filter_test_combinations = [
                            # All filter are set to their minimum values.
                            # So, we expect to get all 4 trips in current test data with
                            (7, 0.0, 1, 50000, 1, ["trip1", "trip2", "trip3", "trip4"], traveler_checkins),

                            # Trip2 has a large unchecked gap. So we expect it to have large Inter streak days value
                            # comparing to other trip. So we expect to filter out trip2 with these filter values
                            (7, 0.2, 0.4, 50000, 1, ["trip1", "trip3", "trip4"], traveler_checkins),

                            # Trip 3 has an implausible speed value between a transition, so we set the maximum speed to
                            # 3500 km/h. Reference: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0148913
                            (7, 0.2, 1, 1500, 1, ["trip1", "trip2", "trip4"], traveler_checkins),

                            # this trip demonstrate filtering trip by the minimum duration.
                            # Trip3 is 13 days longer and we expect to filter it out using min_duration as 14 days
                            (14, 0.2, 1, 50000, 1, ["trip1", "trip2", "trip4"], traveler_checkins),
                            ]

@pytest.mark.parametrize('min_duration, min_density, max_inter_streak_days, max_speed, max_checkin_discontinuity, '
                         'expected_trips, traveler_checkins', filter_test_combinations)
def test_all_filters(min_duration, min_density, max_inter_streak_days, max_speed, max_checkin_discontinuity,
                     expected_trips, traveler_checkins):
    """
    This is a parameterized test to test mined trips using different quality filters
    """
    generated_trips = Traveler.from_checkins(traveler_checkins,
                                             'twitter',
                                             min_duration=min_duration,
                                             min_density=min_density,
                                             max_inter_streak_days=max_inter_streak_days,
                                             max_speed=max_speed,
                                             max_checkin_discontinuity=max_checkin_discontinuity).trips
    assert set([trip_name_id_map[exp] for exp in expected_trips]) == set([trip.trip_id for trip in generated_trips])