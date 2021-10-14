import functools
import operator

from tripmining.model.coordinate import Coordinate


class Location:
    """
    A place where users can check in.
    """

    def __init__(self, location_id: str, coordinate: Coordinate, country_code: str, category: str = '', geonames_id: str = '', name: str = ''):
        self.location_id = location_id
        self.lat = coordinate.lat
        self.lng = coordinate.lng
        self.country_code = country_code
        self.category = category
        self.geonames_id = geonames_id
        self.name = name

    def __hash__(self) -> int:
        hashes = map(hash, (self.location_id, self.lat, self.lng, self.category, self.country_code))
        return functools.reduce(operator.xor, hashes)

    def __str__(self) -> str:
        return f"{self.name if self.name else ''}#{self.location_id} in {self.country_code} at ({self.lat}, {self.lng})"

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if isinstance(other, self.__class__):
            if self.location_id == other.location_id:
                return True
            if self.lat != other.lat:
                return False
            if self.lng != other.lng:
                return False
            if self.category != other.category:
                return False
            if self.country_code != other.country_code:
                return False
            return True
        return False
