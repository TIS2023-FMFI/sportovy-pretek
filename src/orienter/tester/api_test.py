import unittest

from ..commander.utils import get_clubs, get_races_in_month
from ..communicator.api import API
from ..configurator import configuration


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        if not configuration.API_KEY:
            raise unittest.SkipTest("no API key configured")
        self.api = API(configuration.API_KEY, configuration.API_ENDPOINT)

    def test_api_get_category_list(self):
        self.assertIsNotNone(self.api.get_category_list())

    def test_get_clubs(self):
        clubs = get_clubs(self.api)
        self.assertTrue(clubs, 'failed to retrieve any clubs')

    def test_get_races_in_month(self):
        for month in range(1, 13):
            races = get_races_in_month(self.api, month)
            if races:
                break
        else:
            self.assertTrue(False, 'failed to retrieve any races for the next twelve months')
