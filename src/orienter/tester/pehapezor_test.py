import re
import socket
import unittest
from unittest import SkipTest

from sqlalchemy import select

from ..configurator.config import configuration
from ..databasor import models
from ..databasor import pehapezor, schemas
from ..databasor.session import Session


class PehapezorTestCase(unittest.TestCase):
    def setUp(self):
        p = re.compile(r"^(?:https?://)?(?:[^@/]+@)?([^:/]+)(?::([0-9]+))?.*$", re.I | re.M)
        m = p.match(configuration.WEB_APP_URL)
        self.assertIsNotNone(m, 'invalid WEB_APP_URL in configuration')

        hostname, port = m.groups()[0], int(m.groups()[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((hostname, port))
        except Exception:
            raise SkipTest("failed to connect to pehapezor server, skipping pehapezor tests")
        finally:
            s.close()

    def test_select_competitions(self):
        with Session.begin() as session:
            stmt = select(models.Competition)
            competitions_objs = pehapezor.exec_select(stmt)
            self.assertTrue(competitions_objs)
            competition_schema = schemas.CompetitionSchema()
            competitions = [competition_schema.load(obj, session=session) for obj in competitions_objs]
            self.assertTrue(competitions)
