import datetime
import logging
import os
from collections.abc import Generator
from io import StringIO

import pandas

from tripmining.model.checkin import Checkin
from tripmining.model.coordinate import Coordinate
from tripmining.model.location import Location


class CheckInParser:
    def __init__(self, checkin_file: str):
        if not os.path.isfile(checkin_file):
            raise ValueError(f'File {checkin_file} is not a regular file.')
        self.checkin_file = checkin_file

    def parse(self) -> Generator:
        with open(self.checkin_file, 'r', encoding="UTF-8") as f:
            for line in f:
                try:
                    yield from self.parse_line(line)
                except ValueError as e:
                    logging.warning(f'Skipping line: {line}', e)

    def parse_line(self, line):
        user_id, city_name, city_geonames_id, latitude, longitude, country_code, checkin_time, category_name, root_category = pandas.read_csv(StringIO(line))
        yield Checkin(user_id, Location('GEON::' + city_geonames_id, Coordinate(latitude, longitude), country_code, category=root_category, name=city_name),
                      self.parse_date(checkin_time))

    @staticmethod
    def parse_date(checkin_time):
        try:
            date = datetime.datetime.strptime(f'{checkin_time.strip()}', '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            try:
                date = datetime.datetime.strptime(f'{checkin_time.strip()}', '%Y-%m-%dT%H:%M')
            except ValueError:
                date = datetime.datetime.strptime(f'{checkin_time.strip()}', '%Y-%m-%d %H:%M:%S.0')
        return date
