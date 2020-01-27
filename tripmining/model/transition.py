from geopy import distance


class Transition:
    """
    Captures transitions in between the blocks
    """

    def __init__(self, from_location, to_location, time_difference):
        self.from_location = from_location
        self.to_location = to_location
        self.time = self.__time(time_difference)
        self.distance = self.__distance()
        self.speed = self.__speed()

    def __distance(self) -> float:
        return distance.distance((self.from_location.lat, self.from_location.lng),
                                 (self.to_location.lat, self.to_location.lng)).km

    def __time(self, time_difference) -> float:
        return time_difference.days * 24 + time_difference.seconds / 3600

    def __speed(self) -> float:
        # or some traverlers the very first checkin is not at home, so it will be at a block
        # the time difference is zero in such cases, so this code returns minus values to indicate such scenarios
        if self.time == 0:
            return -1.0
        return self.distance / self.time

    def to_json(self):
        return f"""{{
      "from_location_lat": "{self.from_location.lat}",
      "from_location_lng": "{self.from_location.lng}",
      "to_location_lat": "{self.to_location.lat}",
      "to_location_lng": "{self.to_location.lng}",
      "distance": "{self.distance}",
      "time": "{self.time}",
      "speed": "{self.speed}",
    }}"""

    def to_dict(self):
        return {
            "from_location_lat": self.from_location.lat,
            "from_location_lng": self.from_location.lng,
            "to_location_lat": self.to_location.lat,
            "to_location_lng": self.to_location.lng,
            "distance": self.distance,
            "time": self.time,
            "speed": self.speed
            }
