import datetime

from astral import sun, LocationInfo
from astral.location import Location, Observer

from tripmining.model.coordinate import Coordinate


def day_length(date: datetime, coordinate: Coordinate):
    """
    :param date: A date or datetime object of the day in question.
    :param coordinate: the position on the globe
    :return: a floating point duration of the day at
    """
    try:
        sunrise, sunset = sun.daylight(Observer(coordinate.lat, coordinate.lng), date)
    except ValueError:
        # check if sun in above or below horizon
        if Location(LocationInfo(latitude=coordinate.lat, longitude=coordinate.lng)).solar_elevation(date) > 0:
            return 24
        else:
            return 0
    return (sunset - sunrise) / datetime.timedelta(hours=1)
