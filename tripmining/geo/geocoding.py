import os
import sys

from geopy import distance

from tripmining.model.city import City
from tripmining.model.coordinate import Coordinate
from tripmining.preprocessing.parser.geonames_cities_parser import CitiesParser

LOW_ACCURACY_CITIES = os.path.join('dataset', 'cities15000.txt')


def distance_to(start, destination) -> float:
    return distance.distance((start.lat, start.lng), (destination.lat, destination.lng)).km


class CityGeoCoder:
    """
    Geocodes a coordinate to the nearest city. This class is quite inefficient and should only be used for small input sizes.
    """

    def __init__(self):
        self.cities = set(CitiesParser(LOW_ACCURACY_CITIES).parse())

    def closest_city(self, position: Coordinate) -> City:
        """
        Given a postition it returns the nearest city
        :param position: the query position
        :return: the nearest city
        """

        distance: int = sys.maxsize
        for city in self.cities:
            current_distance = distance_to(Coordinate(city.lat, city.lng), position)
            if current_distance < distance:
                distance = current_distance
                closest_candidate = city
        return closest_candidate
