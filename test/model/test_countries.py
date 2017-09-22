from unittest import TestCase

from tripmining.model.countries import Countries, Country


class TestCountries(TestCase):
    def setUp(self):
        self.countries = Countries()

    def test_get_by_iso_DE(self):
        self.assertEqual(Country("Germany", "DE"), self.countries.get_by_iso("DE"))

    def test_get_by_iso_EG(self):
        self.assertEqual(Country("Egypt", "EG"), self.countries.get_by_iso("EG"))

    def test_get_by_iso_AU(self):
        self.assertEqual(Country("Australia", "AU"), self.countries.get_by_iso("AU"))

    def test_get_by_iso(self):
        self.assertEqual(Country("Kuwait", "KW"), self.countries.get_by_iso("KW"))

    def test_get_by_name(self):
        self.assertEqual(Country("Hungary", "HU"), self.countries.get_by_name('Hungary'))
