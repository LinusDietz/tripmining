from sortedcontainers import SortedList

from tripmining.model.checkin import Checkin
from tripmining.model.location import Location


class Block:
    def __init__(self, checkins: list):
        self.checkins = SortedList(checkins, key=lambda c: c.date)
        self.country_code = self.first_checkin().location.country_code

    def first_checkin(self) -> Checkin:
        return self.checkins[0]

    def last_checkin(self) -> Checkin:
        return self.checkins[-1]

    def duration(self) -> int:
        """
        :return: The duration of the block in days
        """
        if len(self.checkins) < 2:
            return 1

        return (self.last_checkin().date.date() - self.first_checkin().date.date()).days + 1

    def to_json(self):
        return f"""{{
      "country_code": "{self.country_code}",
      "location_name": "{self.first_checkin().location.name}",
      "location_id": "{self.first_checkin().location.location_id}",
      "first_checkin": "{self.first_checkin().date}",
      "last_checkin": "{self.last_checkin().date}",
      "duration": {self.duration()},
      "num_checkins": {len(self.checkins)}
    }}"""

    def to_dict(self):
        block_location: Location = self.first_checkin().location
        return {"country_code": self.country_code,
                "location_name": block_location.name,
                "location_id": block_location.location_id,
                "location_latitude": block_location.lat,
                "location_longitude": block_location.lng,
                "first_checkin": self.first_checkin().date,
                "last_checkin": self.last_checkin().date,
                "duration": self.duration(),
                "num_checkins": len(self.checkins)}

    def to_json_with_checkins(self):
        checkins: str = ',\n    '.join([checkin.to_json() for checkin in self.checkins])
        return f"""{{
      "country_code": "{self.country_code}",
      "location_name": "{self.first_checkin().location.name}",
      "location_id": "{self.first_checkin().location.location_id}",
      "first_checkin": "{self.first_checkin().date}",
      "last_checkin": "{self.last_checkin().date}",
      "duration": {self.duration()},
      "num_checkins": {len(self.checkins)},
      "checkins": [
        {checkins}
      ]
    }}"""
