from collections import Counter

from sortedcontainers import SortedList

from tripmining.model.checkin import Checkin
from tripmining.model.location import Location


class User:

    def __init__(self, user_id, checkins, dataset):
        self.user_id: str = user_id
        self.dataset: str = dataset
        if (len(set([c.user for c in checkins]))) > 1:
            raise ValueError("Not all checkins provided are from the same user!")
        self.checkins: SortedList = SortedList(checkins, lambda c: c.date)
        self.home_location = self.calculate_home_location()
        self.home_country = self.calculate_home_country()
        self.ratio_checkins_home = (len(list(filter(lambda ci: self.checkin_at_home_location(ci), self.checkins))) / len(self.checkins))

    def checkin_at_home_country(self, checkin: Checkin):
        """
        Determines whether a given checkin was done at home.
        :param checkin:
        :return: True if the checkin was done in the travelers's home country false otherwise
        """
        return self.home_country == checkin.location.country_code

    def has_clear_home_location(self, use_segmentation_id=False, threshold: float = 0.5):
        if use_segmentation_id:
            if not all(map(lambda ci: ci.location.segmentation_id, self.checkins)):
                raise ValueError("Not all checkins have a segmentation_id")
            user_location_count = Counter(map(lambda ci: ci.location.segmentation_id, self.checkins))
            home = max(user_location_count, key=user_location_count.get)
            return user_location_count[home] / sum(user_location_count.values()) > threshold

        return self.ratio_checkins_home >= threshold

    def calculate_home_location(self) -> Location:
        user_locations = Counter(map(lambda ci: ci.location.location_id, self.checkins))
        return max(user_locations, key=user_locations.get)

    def calculate_home_country(self) -> str:
        """
        :return: the country code of the user's residence
        """
        user_countries = Counter(map(lambda ci: ci.location.country_code, self.checkins))
        return max(user_countries, key=user_countries.get)

    def is_last_checkin(self, checkin) -> bool:
        return self.checkins[-1] == checkin

    def checkin_at_home_location(self, checkin: Checkin) -> bool:
        """
        Determines whether a given checkin was done at home.
        :param checkin:
        :return: True if the checkin was done in the travelers's home country false otherwise
        """
        return self.home_location == checkin.location
