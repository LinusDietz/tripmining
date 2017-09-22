import functools
import operator

from tripmining.model.coordinate import Coordinate
from tripmining.model.location import Location


class City(Location):
    def __init__(self, name: str, location_id: str, lat: float, lng: float, country_code: str):
        self.name = name
        super().__init__(location_id, Coordinate(lat, lng), country_code)

    def __str__(self) -> str:
        return f"City {self.name} ({self.country_code}) at ({self.lat}, {self.lng})"

    def __hash__(self) -> int:
        hashes = map(hash, (self.lat, self.lng, self.country_code, self.name))
        return functools.reduce(operator.xor, hashes)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if isinstance(other, self.__class__):
            if self.lat != other.lat:
                return False
            if self.lng != other.lng:
                return False
            if self.name != other.name:
                return False
            if self.country_code != other.country_code:
                return False
            return True
        return False
