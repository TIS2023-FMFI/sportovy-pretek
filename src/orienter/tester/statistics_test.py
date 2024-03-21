import unittest

from ..statista.statistics import Generator, YEAR_AGO


class StatisticsTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = Generator()

    def test_generate_one_racer(self):
        with open("test_one_racer.html", "w", encoding="UTF-8") as html:
            html.write(self.generator.render([("Andrea", "Papugová")], since=YEAR_AGO))

    def test_generate_multiple_racers(self):
        with open("test_multiple_racers.html", "w", encoding="UTF-8") as html:
            html.write(
                self.generator.render(
                    [
                        ("Andrea", "Papugová"),
                        ("Karol", "Janšo"),
                        ("Peter", "Kotuliak"),
                        ("Andrej", "Mikloš"),
                        ("Maria", "Dubynets"),
                        ("Iveta", "Putnovská"),
                    ],
                    since=YEAR_AGO,
                )
            )
