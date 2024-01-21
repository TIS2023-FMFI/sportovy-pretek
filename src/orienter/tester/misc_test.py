import unittest

from ..commander.utils import encode_competition_id, decode_competition_id


class MiscTestCase(unittest.TestCase):
    def test_encode_decode_competition_id(self):
        comp_id_orig, event_id_orig = 123, 987
        encoded_id = encode_competition_id(comp_id_orig, event_id_orig)
        comp_id_decoded, event_id_decoded = decode_competition_id(encoded_id)
        self.assertEqual(comp_id_orig, comp_id_decoded)
        self.assertEqual(event_id_orig, event_id_decoded)
