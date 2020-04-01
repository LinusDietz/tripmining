from tripmining.model.countries import Countries
from tripmining.model.location import Location
from tripmining.model.trip import Trip
from tripmining.model.user import User


class Traveler:

    def __init__(self, user: User, checkin_streaks_gap=3, min_duration=7, min_density=0.2, filter_continent=''):
        self.countries = Countries()
        self.user_id = user.user_id
        self.dataset = user.dataset
        self.min_duration = min_duration
        self.min_density = min_density
        self.home_location: Location = user.home_location
        self.ratio_checkins_home = user.ratio_checkins_home
        self.home_country_code = user.home_country
        self.trips = set()
        self.filter_continent = filter_continent
        self.__extract_trips(user, checkin_streaks_gap)

    def __get_filtered_sorted_checkins(self, user_checkins):
        return filter(lambda x: self.filter_continent == '' or self.countries.get_by_iso(
            x.location.country_code).continent == self.filter_continent,
                      user_checkins)

    def __extract_trips(self, user: User, checkin_streaks_gap):
        """
        This method segments the traveler's checkin stream into trips.
        :param user:
        :return: a list of trips
        """
        current_travel_checkins = list()
        for checkin in self.__get_filtered_sorted_checkins(user.checkins):
            if user.checkin_at_home_location(checkin) or user.is_last_checkin(checkin):
                # Travel is ended due to home checkin or end of user checkin stream
                # only append if there are checkins in the trip.
                if current_travel_checkins:
                    trip = Trip(self, current_travel_checkins, checkin_streaks_gap)
                    if self.min_duration <= trip.duration() and self.min_density <= trip.checkin_density():
                        self.trips.add(trip)

                # clear current trip
                current_travel_checkins = list()
                continue

            # Travel is ongoing
            current_travel_checkins.append(checkin)

    @staticmethod
    def from_user(user: User, min_duration: int = 7, min_density: float = 0.2, filter_continent=''):
        return Traveler(user, min_duration=min_duration, min_density=min_density, filter_continent=filter_continent)

    @staticmethod
    def from_checkins(checkins, dataset, checkin_streaks_gap=3, min_duration: int = 7, min_density: float = 0.2,
                      filter_continent=''):
        if not checkins:
            raise ValueError("Cannot create a traveler with zero check-ins")
        if not dataset:
            raise ValueError("Cannot create a traveler without a dataset identifier")

        user = User(checkins[0].user, checkins, dataset)
        return Traveler(user, checkin_streaks_gap, min_duration=min_duration, min_density=min_density,
                        filter_continent=filter_continent)

    def __str__(self):
        return f"Traveler {self.user_id} from {self.home_location}, with {len(self.trips)} trips."

    @staticmethod
    def csv_header():
        return "user_id, dataset, home_location, home_country_code, num_trips, home_checkins\n"

    def to_csv(self):
        return f'{self.user_id}, {self.dataset}, "{str(self.home_location.name)}", {self.home_country_code}, {len(self.trips)}, {self.ratio_checkins_home}\n'
