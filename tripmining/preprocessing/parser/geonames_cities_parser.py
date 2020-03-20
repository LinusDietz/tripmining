import logging
import os
from collections.abc import Generator

from tripmining.model.city import City


class CitiesParser:
    def __init__(self, cities_file: str):
        if not os.path.isfile(cities_file):
            raise ValueError(f'File {cities_file} is not a regular file.')
        self.cities_file = cities_file

    def parse(self) -> Generator:
        logging.info(f"Parsing {self.cities_file}...")

        with open(self.cities_file, 'r', encoding="UTF8") as in_file:
            for line in in_file:
                try:
                    yield CitiesLineParser(line).parse()
                except ValueError as e:
                    logging.warning(f'Skipping line: {line}', e)


class CitiesLineParser:
    def __init__(self, line: str):
        raw_split = line.split('\t')
        if len(raw_split) != 19:
            raise ValueError(f'Malformed line. Has {len(raw_split)} instead of 19 elements:\n{line}')
        self.line_split = raw_split

    def parse(self) -> City:
        geoname_id, name, ascii_name, alternate_names, latitude, longitude, feature_class, feature_code, country_code, cc2, admin1_code, admin2_code, admin3_code, admin4_code, population, elevation, dem, timezone, modification_date = self.line_split
        return City(name, geoname_id, latitude, longitude, country_code)
