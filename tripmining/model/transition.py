from geopy import distance


class Transition:
    """
    Captures transitions in between the blocks
    """

    def __init__(self, from_location, to_location, time_difference):
        self.from_location = from_location
        self.to_location = to_location
        self.time = time_difference
        self.speed = self.__speed()

    def __speed(self) -> float:
        # or some traverlers the very first checkin is not at home, so it will be at a block
        # the time difference is zero in such cases, so this code returns minus values to indicate such scenarios
        transition_time = self.time.total_seconds()//3600
        if transition_time == 0:
            return -1.0
        transition_distance = distance.distance((self.from_location.lat, self.from_location.lng),
                                 (self.to_location.lat, self.to_location.lng)).km
        return transition_distance / transition_time

    def to_json(self):
        return f"""{{
      "from_location_lat": "{self.from_location.lat}",
      "from_location_lng": "{self.from_location.lng}",
      "to_location_lat": "{self.to_location.lat}",
      "to_location_lng": "{self.to_location.lng}",
      "time": "{self.time.total_seconds()//3600}",
      "speed": "{self.speed}",
    }}"""

    def to_dict(self):
        return {
            "from_location_lat": self.from_location.lat,
            "from_location_lng": self.from_location.lng,
            "to_location_lat": self.to_location.lat,
            "to_location_lng": self.to_location.lng,
            "time": self.time.total_seconds()//3600,
            "speed": self.speed
            }
