import unittest

from ..communicator.api import API
from ..configurator import configuration


class ApiTestCase(unittest.TestCase):
    def test_api_communication(self):
        if not configuration.API_KEY:
            raise unittest.SkipTest("no API key configured")
        api = API(configuration.API_KEY, configuration.API_ENDPOINT)
        self.assertIsNotNone(api.get_category_list())
