import unittest

from tripmining.geo.geocoding import CityGeoCoder
from tripmining.model.coordinate import Coordinate


class TestCountryGeocoder(unittest.TestCase):

    def setUp(self):
        self.geo_coder = CityGeoCoder()

    def test_munich_in_DE(self):
        self.assertEqual("DE", self.geo_coder.closest_city(Coordinate(48.1351, 11.5820)).country_code)

    def test_new_york_city_in_US(self):
        self.assertEqual("US", self.geo_coder.closest_city(Coordinate(40.7128, -74.0060)).country_code)

    def test_fiji_in_FJ(self):
        self.assertEqual("FJ", self.geo_coder.closest_city(Coordinate(-17.644438, 178.049347)).country_code)

    def test_stlawrence_alaska_in_US(self):
        self.assertEqual("US", self.geo_coder.closest_city(Coordinate(63.639875, -170.436122)).country_code)

    def test_kamchatka_in_RU(self):
        self.assertEqual("RU", self.geo_coder.closest_city(Coordinate(57.791474, 160.235901)).country_code)
