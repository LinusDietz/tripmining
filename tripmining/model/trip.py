import hashlib
import math
from collections import Counter

import numpy as np
import pkg_resources
from sortedcontainers import SortedList

from tripmining.geo.geocoding import distance_to
from tripmining.model.block import Block
from tripmining.model.checkin import Checkin


class Trip:
    """
    A Trip is the sequence of all contiguous check-ins a user made abroad.
    """

    def __init__(self, traveler, checkins: list):
        self.traveler = traveler
        self.checkins = SortedList(checkins, key=lambda c: c.date)
        self.trip_id = hashlib.sha1((str(traveler.user_id) + str(self.checkins[0].date) + str(self.checkins[-1].date)).encode('utf-8')).hexdigest()[:10]
        self.blocks = self.__get_blocks()

    def first_checkin(self) -> Checkin:
        return self.checkins[0]

    def last_checkin(self) -> Checkin:
        return self.checkins[-1]

    def is_domestic(self) -> str:
        if len(self.countries()) > 1:
            return 'FALSE'
        if self.traveler.home_country_code == self.first_checkin().location.country_code:
            return 'TRUE'
        else:
            return 'FALSE'

    def duration(self) -> int:
        """
        :return: The duration of the travel in calendar days
        """
        if len(self.checkins) < 2:
            return 1

        return (self.last_checkin().date.date() - self.first_checkin().date.date()).days + 1

    def checkin_density(self) -> float:
        """
        :return: The density of a trip. This is defined as the fraction of days with a checkin.
        """
        return len(set([checkin.date.date() for checkin in self.checkins])) / self.duration()

    def radius_of_gyration(self) -> float:
        """
        Returns the radius of gyration
        """

        def great_circle_distance(pt1, pt2):
            """
            Return the great-circle distance in kilometers between two points,defined by a tuple (lat, lon).
            """
            r = 6371.

            delta_latitude = math.radians(pt1[0] - pt2[0])
            delta_longitude = math.radians(pt1[1] - pt2[1])
            latitude1 = math.radians(pt1[0])
            latitude2 = math.radians(pt2[0])

            a = math.sin(delta_latitude / 2) ** 2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(delta_longitude / 2) ** 2
            return r * 2. * math.asin(math.sqrt(a))

        d = Counter((ci.location.lat, ci.location.lng) for ci in self.checkins)
        sum_weights = sum(d.values())
        positions = list(d.keys())  # Unique positions

        if len(positions) == 0:
            return None

        barycenter = [0, 0]
        for pos, t in d.items():
            barycenter[0] += pos[0] * t
            barycenter[1] += pos[1] * t

        barycenter[0] /= sum_weights
        barycenter[1] /= sum_weights

        r = 0.
        for pos, t in d.items():
            r += float(t) / sum_weights * \
                 great_circle_distance(barycenter, pos) ** 2
        return math.sqrt(r)

    def checkin_frequency(self) -> float:
        """
        :return: The checkin frequency of a trip.
        """
        return len(self.checkins) / self.duration()

    def countries(self) -> set:
        """
        :return: The a set of countries the trip spans
        """
        return set([checkin.location.country_code for checkin in self.checkins])

    def locations(self) -> set:
        """
        :return: The a set of locations the trip spans
        """
        return set([f"{checkin.location.country_code}:{checkin.location.location_id}" for checkin in self.checkins])

    def location_ids(self) -> set:
        """
        :return: The a set of locations the trip spans by id
        """
        return set([f"{checkin.location.location_id}" for checkin in self.checkins])

    def unique_locations(self) -> set:
        """
        :return: The a set of location objects the trip spans
        """
        return set([checkin.location for checkin in self.checkins])

    def checkin_distances(self) -> list:
        """
        :return: Distance between checkins, in kilometers
        """
        return [distance_to(c1.location, c2.location) for c1, c2 in zip(self.checkins, self.checkins[1:])]

    def checkin_durations(self) -> list:
        """
        :return: Duration of checkins, in minutes
        """
        return [dt.total_seconds() / 60. for dt in np.diff([checkin.date for checkin in self.checkins])]

    def checkin_displacements(self):
        return [(distance_to(self.traveler.home_location, checkin.location)) for checkin in self.checkins]

    def mean_checkin_distance(self) -> float:
        """
        :return: The mean distance between two checkins
        """
        return np.mean(self.checkin_distances())

    def median_checkin_distance(self) -> float:
        """
        :return: The mean distance between two checkins
        """
        return np.median(self.checkin_distances())

    def std_checkin_distance(self) -> float:
        """
        :return: The mean distance between two checkins
        """
        return np.std(self.checkin_distances())

    def mean_checkin_duration(self) -> float:
        """
        :return: The mean duration between two checkins in minutes
        """
        return np.mean(self.checkin_durations())

    def median_checkin_duration(self) -> float:
        """
        :return: The mean duration between two checkins in minutes
        """
        return np.median(self.checkin_durations())

    def std_checkin_duration(self) -> float:
        """
        :return: The mean duration between two checkins in minutes
        """
        return np.std(self.checkin_durations())

    def mean_displacement(self) -> float:
        """
        :return: The mean distance between the user's home and the checkins
        """
        return np.mean(self.checkin_displacements())

    def median_displacement(self) -> float:
        """
        :return: The median distance between the user's home and the checkins
        """
        return np.median(self.checkin_displacements())

    def std_displacement(self) -> float:
        """
        :return: The std of the distance between the user's home and the checkins
        """
        return np.std(self.checkin_displacements())

    def get_location_for_location_id(self, location_id):
        for checkin in self.checkins:
            if checkin.location.location_id == location_id:
                return checkin.location

    def to_csv(self):
        return f"""{self.traveler.dataset}, \"{self.traveler.user_id}\", \"{self.trip_id}\", \"{self.traveler.home_country_code}\", {self.is_domestic()}, {self.first_checkin().date}, {self.last_checkin().date}, {self.duration()}, {len(
            self)}, {len(self.blocks)}, {len(set([ci.location for ci in self.checkins]))}, {self.checkin_density()}, {self.checkin_frequency()}, {len(
            self.countries())}, {self.mean_checkin_distance()}, {self.mean_checkin_duration()}, {self.mean_displacement()}, {self.radius_of_gyration()}, {len(
            self.categorical_checkins("Food"))}, {len(self.categorical_checkins("Nightlife Spot"))}, {len(
            self.categorical_checkins("Arts & Entertainment"))}, {len(self.categorical_checkins("Outdoors & Recreation"))}\n"""

    def __len__(self):
        return len(self.checkins)

    def __str__(self):
        return f"Trip of {self.traveler.user_id} from {self.checkins[0].date} to {self.checkins[-1].date} covering {{{self.locations()}}} "

    @staticmethod
    def csv_header():
        return "dataset, traveler_id, trip_id, traveler_home, is_domestic, first_checkin, last_checkin, duration, num_checkins, num_blocks, num_locations, checkin_density, checkin_frequency, num_countries, mean_checkin_distance, mean_checkin_duration, mean_displacement, radius_of_gyration, food_checkins, nightlife_checkins, arts_checkins, outdoors_checkins\n"

    def to_dict_small(self) -> dict:
        return {"trip_id": self.trip_id,
                "traveler_id": self.traveler.user_id,
                "dataset": self.traveler.dataset,
                "traveler_home": self.traveler.home_country_code,
                "first_checkin": str(self.first_checkin().date),
                "last_checkin": str(self.last_checkin().date),
                "duration": self.duration(),
                "tripmining_version": pkg_resources.get_distribution("tripmining").version}

    def to_dict(self):
        blocks: list = [block.to_dict() for block in self.blocks]
        checkin_distances = self.checkin_distances()
        displacements = self.checkin_displacements()
        durations = self.checkin_durations()
        return {"trip_id": self.trip_id,
                "traveler_id": self.traveler.user_id,
                "dataset": self.traveler.dataset,
                "traveler_home_country": self.traveler.home_country_code,
                "traveler_home_location": self.traveler.home_location.name,
                "traveler_home_location_id": self.traveler.home_location.location_id,
                "traveler_home_location_lat": self.traveler.home_location.lat,
                "traveler_home_location_lng": self.traveler.home_location.lng,
                "traveler_home_ratio": self.traveler.ratio_tweets_home,
                "first_checkin": self.first_checkin().date,
                "last_checkin": self.last_checkin().date,
                "duration": self.duration(),
                "num_checkins": len(self),
                "blocks": blocks,
                "checkin_density": self.checkin_density(),
                "checkin_frequency": self.checkin_frequency(),
                "num_distinct_countries": len(self.countries()),
                "num_blocks": len(self.blocks),
                "mean_checkin_distance": np.mean(checkin_distances),
                "median_checkin_distance": np.median(checkin_distances),
                "std_checkin_distance": np.std(checkin_distances),
                "mean_checkin_duration": np.mean(durations),
                "median_checkin_duration": np.median(durations),
                "std_checkin_duration": np.std(durations),
                "mean_displacement": np.mean(displacements),
                "median_displacement": np.median(displacements),
                "std_displacement": np.std(displacements),
                "radius_of_gyration": self.radius_of_gyration(),
                "tripmining_version": pkg_resources.get_distribution("tripmining").version}

    def to_json(self):
        blocks: str = ',\n    '.join([block.to_json() for block in self.blocks])
        checkin_distances = self.checkin_distances()
        displacements = self.checkin_displacements()
        durations = self.checkin_durations()
        return f"""{{
  "trip_id": "{self.trip_id}",
  "traveler_id": "{self.traveler.user_id}",
  "dataset": "{self.traveler.dataset}",       
  "traveler_home_country": "{self.traveler.home_country_code}",      
  "traveler_home_location": "{self.traveler.home_location.name}",
  "first_checkin": "{self.first_checkin().date}",
  "last_checkin": "{self.last_checkin().date}",
  "duration": {self.duration()},
  "num_checkins": {len(self)},
  "checkin_density": {format(self.checkin_density(), '.2f')},
  "checkin_frequency": {format(self.checkin_frequency(), '.2f')},
  "num_distinct_countries": {len(self.countries())},
  "num_blocks": {len(self.blocks)},
  "blocks": [
    {blocks}
  ],
  "mean_checkin_distance": {format(np.mean(checkin_distances), '.2f')},
  "median_checkin_distance": {format(np.median(checkin_distances), '.2f')},
  "std_checkin_distance": {format(np.std(checkin_distances), '.2f')},
  "mean_checkin_duration": {format(np.mean(durations), '.2f')},
  "median_checkin_duration": {format(np.median(durations), '.2f')},
  "std_checkin_duration": {format(np.std(durations), '.2f')},
  "mean_displacement": {format(np.mean(displacements), '.2f')},
  "median_displacement": {format(np.median(displacements), '.2f')},
  "std_displacement": {format(np.std(displacements), '.2f')},
  "radius_of_gyration": {format(self.radius_of_gyration(), '.2f')}
}}
"""

    def to_json_with_checkins(self):
        blocks: str = ',\n    '.join([block.to_json_with_checkins() for block in self.blocks])
        checkin_distances = self.checkin_distances()
        displacements = self.checkin_displacements()
        durations = self.checkin_durations()
        return f"""{{
      "trip_id": "{self.trip_id}",
      "traveler_id": "{self.traveler.user_id}",
      "dataset": "{self.traveler.dataset}",       
      "traveler_home_country": "{self.traveler.home_country_code}",      
      "traveler_home_location": "{self.traveler.home_location.name}",
      "first_checkin": "{self.first_checkin().date}",
      "last_checkin": "{self.last_checkin().date}",
      "duration": {self.duration()},
      "num_checkins": {len(self)},
      "checkin_density": {format(self.checkin_density(), '.2f')},
      "checkin_frequency": {format(self.checkin_frequency(), '.2f')},
      "num_distinct_countries": {len(self.countries())},
      "num_blocks": {len(self.blocks)},
      "blocks": [
        {blocks}
      ],
      "mean_checkin_distance": {format(np.mean(checkin_distances), '.2f')},
      "median_checkin_distance": {format(np.median(checkin_distances), '.2f')},
      "std_checkin_distance": {format(np.std(checkin_distances), '.2f')},
      "mean_checkin_duration": {format(np.mean(durations), '.2f')},
      "median_checkin_duration": {format(np.median(durations), '.2f')},
      "std_checkin_duration": {format(np.std(durations), '.2f')},
      "mean_displacement": {format(np.mean(displacements), '.2f')},
      "median_displacement": {format(np.median(displacements), '.2f')},
      "std_displacement": {format(np.std(displacements), '.2f')},
      "radius_of_gyration": {format(self.radius_of_gyration(), '.2f')}
    }},
"""

    def __get_blocks(self) -> SortedList:
        blocks = list()
        first_checkin = self.checkins[0]
        current_checkins = [first_checkin]
        current_location = first_checkin.location.location_id
        for checkin in self.checkins[1:]:
            if current_location == checkin.location.location_id:
                current_checkins.append(checkin)
            else:
                blocks.append(Block(current_checkins))
                current_checkins = [checkin]
                current_location = checkin.location.location_id

        blocks.append(Block(current_checkins))
        return SortedList(blocks, key=lambda b: b.first_checkin().date)

    def categorical_checkins(self, category):
        return list(filter(lambda ci: ci.location.category == category, self.checkins))
