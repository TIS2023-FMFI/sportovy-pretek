import unittest

from sqlalchemy import select, insert
from ..databasor import models
from ..databasor import pehapezor, schemas
from ..databasor.session import Session


class PehapezorTestCase(unittest.TestCase):
    def test_select_competitions(self):
        with Session.begin() as session:
            stmt = select(models.Competition)
            competitions_objs = pehapezor.exec_select(stmt)
            self.assertTrue(competitions_objs)
            competition_schema = schemas.CompetitionSchema()
            competitions = [competition_schema.load(obj, session=session) for obj in competitions_objs]
            self.assertTrue(competitions)
