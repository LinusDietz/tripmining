import functools
import operator

from tripmining.model.coordinate import Coordinate


class Location:
    """
    A place than can be visited by users.

    Nope that blocks are segmented by comparing location ids.
    Optionally, one can assign a `segmentation_id` based on which the segmentation can be done as well.
    """

    def __init__(self, location_id: str, coordinate: Coordinate, country_code: str, category: str = '', geonames_id: str = '', segmentation_id='',
                 name: str = ''):
        self.location_id = location_id
        self.lat = coordinate.lat
        self.lng = coordinate.lng
        self.country_code = country_code
        self.category = category
        self.geonames_id = geonames_id
        self.segmentation_id = segmentation_id
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
            if self.segmentation_id and self.segmentation_id == other.segmentation_id:
                # the segmentation ID is used for combining different checkins in a larger area, e.g., combining multiple checkins in a city into one block
                return True
            return self.location_id == other.location_id
        return False
