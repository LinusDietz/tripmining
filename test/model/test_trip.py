import datetime
from unittest import TestCase

from tripmining.model.trip import Trip

from tripmining.model.traveler import Traveler

from tripmining.model.coordinate import Coordinate

from tripmining.model.location import Location

from tripmining.model.checkin import Checkin


class TestTrip(TestCase):

    def setUp(self):
        self.testLocation = Location("testLocation", Coordinate(0, 0), "NA")

        self.traveler_checkins = [
            Checkin("testUser", self.testLocation, datetime.datetime.now() - datetime.timedelta(days=10)),
            Checkin("testUser", self.testLocation, datetime.datetime.now() - datetime.timedelta(days=9)),
            Checkin("testUser", self.testLocation, datetime.datetime.now() - datetime.timedelta(days=7)),
            Checkin("testUser", self.testLocation, datetime.datetime.now() - datetime.timedelta(days=5)),
            Checkin("testUser", self.testLocation, datetime.datetime.now() - datetime.timedelta(days=2)),
            Checkin("testUser", self.testLocation, datetime.datetime.now() - datetime.timedelta(days=1))
        ]
        self.traveler = Traveler.from_checkins(self.traveler_checkins, "testDataset")

    def test_create_trip(self):
        trip = Trip(self.traveler, self.traveler_checkins[2:])

        self.assertEqual(4, len(trip.checkins))

    def test_create_trip_speed_no_movement(self):
        trip = Trip(self.traveler, self.traveler_checkins[2:])

        self.assertEqual(-1, trip.speed)

    def test_create_trip_speed(self):
        checkins = self.traveler_checkins[2:]
        checkins.append(Checkin("testUser", Location("testLocation2", Coordinate(0, 1), "NA"), datetime.datetime.now()))
        trip = Trip(self.traveler, checkins)

        self.assertAlmostEqual(4.63, trip.speed, delta=0.01)

    def test_create_trip_speed_no_checkins(self):
        self.assertRaises(ValueError, Trip, self.traveler, [])
