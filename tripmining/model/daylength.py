import datetime

from astral import Astral, AstralError

from tripmining.model.coordinate import Coordinate


def day_length(date: datetime, coordinate: Coordinate):
    """
    :param date: A date or datetime object of the day in question.
    :param coordinate: the position on the globe
    :return: a floating point duration of the day at
    """
    a = Astral()
    try:
        sunrise, sunset = a.daylight_utc(date, coordinate.lat, coordinate.lng)
    except AstralError:
        # check if sun in above or below horizon
        if a.solar_elevation(date, coordinate.lat, coordinate.lng) > 0:
            return 24
        else:
            return 0
    return (sunset - sunrise) / datetime.timedelta(hours=1)
