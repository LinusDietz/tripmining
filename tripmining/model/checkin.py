import datetime
import functools
import operator

from tripmining.model.location import Location


class Checkin:
    """
    Captures a check-in, which is simply a spatio-temporal indication of the presence of a specific user.
    """

    def __init__(self, user: str, location: Location, local_date: datetime):
        self.user = user
        self.location = location
        self.date = local_date

    def __repr__(self):
        return f'<Checkin: User {self.user} at {self.location} on [{self.date}]>'

    def __str__(self):
        return f'<Checkin: User {self.user} at {self.location} on [{self.date}]>'

    def to_json(self):
        return f"""{{
      "location_name": "{self.location.name}",
      "location_id": "{self.location.location_id}",
      "date": "{self.date}"
    }}"""

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        hashes = map(hash, (self.user, self.location, self.date))
        return functools.reduce(operator.xor, hashes)
