import functools
import math
import operator


class Coordinate:
    def __init__(self, lat, lng):
        f_lat = float(lat)
        if math.fabs(f_lat) > 180:
            raise ValueError(f'The latitude must be between -180 and 180 degrees, but was {f_lat}!')
        f_lng = float(lng)
        if math.fabs(f_lng) > 180:
            raise ValueError(f'The longitude must be between -180 and 180 degrees, but was {f_lng}!')

        self.lat = f_lat
        self.lng = f_lng

    def __hash__(self) -> int:
        hashes = map(hash, (self.lat, self.lng))
        return functools.reduce(operator.xor, hashes)

    def __str__(self) -> str:
        return f"({self.lat}, {self.lng})"

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
