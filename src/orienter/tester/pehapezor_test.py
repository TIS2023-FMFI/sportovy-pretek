import re
import socket
import unittest
from unittest import SkipTest

from sqlalchemy import select

from ..commander.utils import get_active_races
from ..configurator.config import configuration
from ..databasor import models
from ..databasor import pehapezor, schemas
from ..databasor.session import Session


class PehapezorTestCase(unittest.TestCase):
    def setUp(self):
        p = re.compile(r"^(https?://)?(?:[^@/]+@)?([^:/]+)(?::([0-9]+))?.*$", re.I | re.M)
        m = p.match(configuration.WEB_APP_URL)
        self.assertIsNotNone(m, 'invalid WEB_APP_URL in configuration')

        hostname = m.groups()[1]
        port = int(m.groups()[2] if m.groups()[2] else 443 if m.groups()[0] == "https://" else 80)
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

    def test_get_active_races(self):
        active_races = get_active_races()
        self.assertTrue(active_races, "This failure is expected if there are no active races in the database.")

    def test_get_racers(self):
        with Session.begin() as session:
            stmt = select(models.User).order_by(models.User.last_name)
            racer_schema = schemas.UserSchema()
            racers_raw = [racer_schema.load(obj, session=session) for obj in pehapezor.exec_select(stmt)]
            self.assertTrue(racers_raw)
