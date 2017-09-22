import functools
import operator
import os

import pandas as pd


class Country:
    """
    A single county
    """

    def __init__(self, name: str, iso_code: str = '', continent: str = ''):
        self.iso_code = iso_code
        self.name = name
        self.continent = continent

    def __str__(self) -> str:
        return f"<Country: {self.name} ({self.iso_code}) ({self.continent})>"

    def __repr__(self) -> str:
        return f"<Country: {self.name} ({self.iso_code}) ({self.continent})>"

    def __hash__(self) -> int:
        hashes = map(hash, (self.iso_code, self.name))
        return functools.reduce(operator.xor, hashes)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if isinstance(other, self.__class__) and (self.iso_code == other.iso_code) and (self.name == other.name):
            return True
        return False


class Countries:
    """
    A collection of a countries in the world.
    """
    def __init__(self):
        self._countries = self.__read_countries()
        self.iso_countries  = {c.iso_code:c for c in self._countries}
        self.name_countries = {c.name:c for c in self._countries}

    @staticmethod
    def __read_countries():
        """
        Reads in the countries from a file.
        :return: a data base of countries in the world
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        relative_path = os.path.join(dir_path, '..', 'dataset', 'countries-continents.csv')

        country_info = pd.read_csv(relative_path)
        return set([Country(name, iso_code=iso_code, continent=region) for iso_code, name, region in zip(country_info['alpha-2'], country_info['name'], country_info['region'])])

    def get_by_iso(self, iso_code: str) -> Country:
        """
        Returns a Country for an country ISO 3166 code.
        :param iso_code: The iso 3166 that represents a country
        :return: A country, none if the ISO Code does not exist
        """
        try:
            country = self.iso_countries[iso_code.strip()]
        except KeyError:
            print(f"Country not found for {iso_code}")
            country = None

        return country

    def get_by_name(self, name: str) -> Country:
        """
        Returns a Country object based on the exact name.
        :param name: the official name of the country.
        :return: A country, none if the name does not match a country in the database
        """
        try:
            country = self.name_countries[name]
        except KeyError:
            raise ValueError(f'There is no country named {name}!')

        return country
