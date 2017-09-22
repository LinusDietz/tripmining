from unittest import TestCase

from tripmining.model.cities import Cities
from tripmining.model.city import City


class TestCities(TestCase):
    def setUp(self):
        self.cities = Cities()

    def test_get_city_by_coordinates(self):
        self.assertEqual(City('Kirwan', 8349354, -19.30323, 146.72531, 'AU'), self.cities.get_city_by_coordinates(-19.30323, 146.72531))

    def test_get_nearest_city(self):
        lat = 22.556200
        lng = 88.375194
        print('%s %s' % (self.cities.get_nearest_city(lat, lng, 'IN')))

    def test_get_nearest_city2(self):
        lat = 22.590057
        lng = 88.481279
        print('%s %s' % (self.cities.get_nearest_city(lat, lng,'IN')))

    def test_get_nearest_city3(self):
        lat = 22.664267
        lng = 88.185607
        print('%s %s' % (self.cities.get_nearest_city(lat, lng,'IN')))

    def test_get_nearest_city4(self):
        lat = 27.089140
        lng = 70.331834
        print('%s %s' % (self.cities.get_nearest_city(lat, lng,'IN')))