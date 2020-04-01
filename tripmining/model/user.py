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

    def has_clear_home_location(self, threshold: float = 0.5):
        return self.ratio_checkins_home >= threshold

    def calculate_home_location(self) -> Location:
        def most_common(location_list: list):
            """
            :param location_list:
            :return: the most common element of the list
            """
            return max(set(location_list), key=location_list.count)

        locations = list(map(lambda c: c.location, self.checkins))
        return most_common(locations)

    def calculate_home_country(self) -> str:
        """
        :return: the country code of the user's residence
        """

        def most_common(countries_list: list):
            """
            :param countries_list:
            :return: the most common element of the list
            """
            return max(set(countries_list), key=countries_list.count)

        countries = list(map(lambda c: c.location.country_code, self.checkins))
        return most_common(countries)

    def is_last_checkin(self, checkin) -> bool:
        return self.checkins[-1] == checkin

    def checkin_at_home_location(self, checkin: Checkin) -> bool:
        """
        Determines whether a given checkin was done at home.
        :param checkin:
        :return: True if the checkin was done in the travelers's home country false otherwise
        """
        return self.home_location == checkin.location
