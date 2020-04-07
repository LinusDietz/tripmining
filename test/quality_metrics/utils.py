import hashlib
import os
import ruamel.yaml as yaml
from tripmining.model.checkin import Checkin
from tripmining.model.coordinate import Coordinate
from tripmining.model.location import Location
import datetime
from datetime import timedelta
import random
import string


def generate_location_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


def generate_home_checkins(user_id, location, from_date, to_date, number_of_checkins):
    """
    Generating some extra checkins to be added before and after a trip. This is to make home location the most frequent
    checked-in location
    :param user_id:
    :param location:
    :param from_date:
    :param to_date:
    :param number_of_checkins:
    :return:
    """
    home_checkins = []
    if not from_date:
        for day in range(number_of_checkins, -1, -1):
            home_checkins.append(Checkin(user=user_id, location=location, local_date=to_date - timedelta(days=day)))
    if not to_date:
        for day in range(number_of_checkins):
            home_checkins.append(Checkin(user=user_id, location=location, local_date=from_date + timedelta(days=day)))
    return home_checkins


def generate_trip_checking(user_id, location, date, number_of_checkins):
    trip_checkins = []
    for checkin in range(number_of_checkins):
        trip_checkins.append(Checkin(user=user_id, location=location, local_date=date))
    return trip_checkins


def generate_checkins(test_data):
    user_home_info = test_data['home']
    last_home_checkin_date = datetime.datetime.strptime(test_data['last_home_before_trip'], '%Y-%m-%d %H:%M:%S')
    first_home_after_trip = datetime.datetime.strptime(test_data['first_home_after_trip'], '%Y-%m-%d %H:%M:%S')
    home_coordinate = Coordinate(lat=user_home_info['location']['lat'], lng=user_home_info['location']['lng'])
    home_location = Location(location_id='23456', country_code=user_home_info['country'], coordinate=home_coordinate,
                             category='admin')
    checkins_before_trip = generate_home_checkins(user_id=test_data['user_id'], location=home_location, from_date=None,
                                                  to_date=last_home_checkin_date, number_of_checkins=10)
    trip_checkins = [] + checkins_before_trip

    for block in test_data['trip']['blocks']:
        block_info = block['block']
        block_coordinate = Coordinate(lat=block_info['location']['lat'], lng=block_info['location']['lng'])
        block_location = Location(location_id=generate_location_id(), coordinate=block_coordinate,
                                  country_code=block_info['location']['code'], category='admin')
        for day in block_info['days']:
            trip_checkins = trip_checkins + generate_trip_checking(test_data['user_id'], block_location,
                                                                   datetime.datetime.strptime(day['day']['date'],
                                                                                              '%Y-%m-%d %H:%M:%S'),
                                                                   day['day']['number_of_checkins'])

    checkins_after_trip = generate_home_checkins(user_id=test_data['user_id'], location=home_location, to_date=None,
                                                 from_date=first_home_after_trip, number_of_checkins=10)
    trip_checkins = trip_checkins + checkins_after_trip
    return trip_checkins


def prepare_chekins_from_raw_data(test_data):
    trip_checkins = generate_checkins(test_data)
    return trip_checkins


def prepare_traveler_from_raw_data(trips: list):
    """
    Construct a traveler by combining a list of single trips
    :param trips:
    :return:
    """
    traveler_chekins = []
    for trip in trips:
        traveler_chekins = traveler_chekins + generate_checkins(trip)
    return sorted(traveler_chekins, key=lambda x: x.date)


def load_trip(trip_name):
    root_dir = os.getcwd()
    with open(os.path.join(os.path.join(os.path.join(root_dir, 'test'), 'quality_metrics'),
                           os.path.join('resources', os.path.join('trips', trip_name + '.yml')))) as file:
        test_data = yaml.load(file, Loader=yaml.Loader)
        return test_data["test"]


def imitate_trip_id(trip):
    """
    Re-producing the trip id which is assiged for each trip in the library. This trip id is mapped with the test name to
    the trip name to verify filtered trips
    :param trip:
    :return:
    """
    return hashlib.sha1((str(trip["user_id"]) + str(prepare_chekins_from_raw_data(trip)[11].date) +
                         str(prepare_chekins_from_raw_data(trip)[-11].date)).encode('utf-8')).hexdigest()[:10]
