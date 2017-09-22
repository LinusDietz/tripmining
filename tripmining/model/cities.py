import os

import scipy.spatial as spatial

from tripmining.model.city import City
from tripmining.preprocessing.parser.geonames_cities_parser import CitiesParser


class Cities:
    """
    A collection of a cities in the world.
    """

    def __init__(self):
        self.cities = list(CitiesParser(os.path.join('dataset', 'cities15000.txt')).parse())
        self.tree = spatial.KDTree(list(map(lambda x: [x.lat, x.lng], self.cities)))

    def get_city_by_coordinates(self, lat, lng):
        matches = list(filter(lambda x: x.lat == lat and x.lng == lng, self.cities))
        if len(matches) == 0:
            return None
        if len(matches) != 1:
            raise ValueError("More than one city found!")
        return matches[0]

    def get_city_by_geonames_id(self, geonames_id):
        matches = list(filter(lambda x: x.location_id == geonames_id, self.cities))
        if len(matches) == 0:
            return None
        if len(matches) != 1:
            raise ValueError("More than one city found!")
        return matches[0]

    def get_nearest_city(self, lat: float, lng: float, country_code: str = '') -> (float, City):
        """
        Returns a City for a pair of coordinates and a country ISO 3166 code.
        :param lat: latitude
        :param lng: longitude
        :param country_code: The iso 3166 that represents a country
        :return: A city, none if the coodinates/ISO Code does not exist
        """
        query_returns = self.tree.query([(lat, lng)])

        if country_code == '' or country_code.strip() == self.cities[query_returns[1][0]].country_code:
            return query_returns[0][0], self.cities[query_returns[1][0]]

        print(f"City not found for {lat}, {lng}, {country_code}")
