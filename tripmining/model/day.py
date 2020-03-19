import datetime


class Day:
    """
    Captures checkin information of each day in the trip
    """
    def __init__(self, date: datetime, number_of_checkins: int):
        self.date = date
        self.number_of_checkins = number_of_checkins

    def to_json(self):
        return f"""{{
        "date" : "{self.date}",
        "number_of_checkins": "{self.number_of_checkins}"
        }}"""
