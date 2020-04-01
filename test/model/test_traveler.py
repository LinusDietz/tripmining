import datetime
from unittest import TestCase

from tripmining.model.coordinate import Coordinate

from tripmining.model.location import Location

from tripmining.model.checkin import Checkin

from tripmining.model.trip import Trip

from tripmining.model.user import User

from tripmining.model.traveler import Traveler

from tripmining.model.cities import Cities
from tripmining.model.city import City


class TestTraveler(TestCase):
    def setUp(self):
        self.testLocation = Location("testLocation", Coordinate(0, 0), "NA")

    def test_create_traveler_without_checkins(self):
        self.assertRaises(ValueError, Traveler.from_checkins,[], "testDataset")

    def test_create_traveler_without_dataset_name(self):
        checkins = [Checkin("testUser", self.testLocation, datetime.datetime.now())]
        self.assertRaises(ValueError, Traveler.from_checkins,checkins, "")

    def test_create_traveler_without_trips(self):
        checkins = [Checkin("testUser", self.testLocation, datetime.datetime.now())]

        traveler = Traveler.from_checkins(checkins, "testDataset")
        self.assertEqual(0, len(traveler.trips))

    def test_create_traveler_to_csv(self):
        checkins = [Checkin("testUser", self.testLocation, datetime.datetime.now())]

        traveler = Traveler.from_checkins(checkins, "testDataset")
        self.assertEqual('testUser, testDataset, "", NA, 0, 1.0\n', traveler.to_csv())
