import datetime
from unittest import TestCase

from tripmining.model.coordinate import Coordinate
from tripmining.model.daylength import day_length

TOLERANCE = 0.2


class TestDaylength(TestCase):
    def test_daylength_equator(self):
        self.assertAlmostEqual(12, day_length(datetime.datetime(2006, 1, 1, 0, 0), Coordinate(0, 0)), delta=TOLERANCE)
        self.assertAlmostEqual(12, day_length(datetime.datetime(2006, 3, 5, 0, 0), Coordinate(0, 90)), delta=TOLERANCE)
        self.assertAlmostEqual(12, day_length(datetime.datetime(2006, 6, 10, 0, 0), Coordinate(0, 180)), delta=TOLERANCE)
        self.assertAlmostEqual(12, day_length(datetime.datetime(2006, 9, 15, 0, 0), Coordinate(0, -90)), delta=TOLERANCE)
        self.assertAlmostEqual(12, day_length(datetime.datetime(2006, 12, 20, 0, 0), Coordinate(0, -180)), delta=TOLERANCE)

    def test_daylength_north_pole_winter(self):
        self.assertAlmostEqual(0, day_length(datetime.datetime(2006, 1, 1, 0, 0), Coordinate(90, 0)), delta=TOLERANCE)

    def test_daylength_north_pole_summer(self):
        self.assertAlmostEqual(24, day_length(datetime.datetime(2018, 6, 21, 0, 0), Coordinate(90, 0)), delta=TOLERANCE)

    def test_daylength_south_pole_winter(self):
        self.assertAlmostEqual(24, day_length(datetime.datetime(2006, 1, 1, 0, 0), Coordinate(-90, 0)), delta=TOLERANCE)

    def test_daylength_south_pole_summer(self):
        self.assertAlmostEqual(0, day_length(datetime.datetime(2018, 6, 21, 0, 0), Coordinate(-90, 0)), delta=TOLERANCE)

    def test_daylength_garching_new_year(self):
        self.assertAlmostEqual(8.4, day_length(datetime.date(2018, 1, 1), Coordinate(48.265, 11.671)), delta=TOLERANCE)

    def test_daylength_garching_summer(self):
        self.assertAlmostEqual(16, day_length(datetime.date(2018, 6, 20), Coordinate(48.265, 11.671)), delta=TOLERANCE)

    def test_daylength_melbourne_christmas(self):
        self.assertAlmostEqual(14.8, day_length(datetime.date(2018, 12, 25), Coordinate(-37.814, 144.963)), delta=TOLERANCE)

    def test_daylength_melbourne_summer(self):
        self.assertAlmostEqual(9.5, day_length(datetime.date(2018, 6, 20), Coordinate(-37.814, 144.963)), delta=TOLERANCE)
