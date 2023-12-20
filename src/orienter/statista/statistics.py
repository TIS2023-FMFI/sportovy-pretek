from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime, timedelta
from html import unescape
from numpy import median
from ..databasor import session
from ..databasor.models import *
from ..commander.utils import DATE_FORMAT, MONTHS_FULL

NOW = datetime.now()
YEAR_AGO = NOW - timedelta(days=365)

env = Environment(
    loader=PackageLoader('orienter.statista'),
    autoescape=select_autoescape()
)

class Loader:
    def __init__(self, racer_id_list, since):
        self.overview = dict()
        self.stats = dict()
        self.since = since
        recent_races = session.session.scalars(session.select(Competition).where(Competition.date > self.since)
                                               .where(Competition.date < NOW)).all()
        for race in recent_races:
            self.stats[race.competition_id] = dict()
            self.stats[race.competition_id]["race_name"] = unescape(race.name)
            self.stats[race.competition_id]["month"] = race.date.month
        for id in racer_id_list:
            self.load_one(id)
    def load_one(self, racer_id):
        self.overview[racer_id] = dict()
        racer = session.session.scalars(session.select(User).where(User.user_id == racer_id)).all()[0]
        racer_name = f"{racer.first_name} {racer.last_name}"
        participations = session.session.scalars(session.select(Signup).where(Signup.user_id == racer_id)).all()
        wins = session.session.scalars(session.select(Performance).where(Performance.user_id == racer_id)
                                       .where(Performance.winner_name == racer_name)).all()
        self.overview[racer_id]["name"] = racer_name
        self.overview[racer_id]["participations"] = len(participations)
        self.overview[racer_id]["wins"] = len(wins)
        self.overview[racer_id]["rank"] = 12345  # TODO replace the DUMMY value with something meaningful

        for race_id in self.stats:
            performance = session.session.scalars(session.select(Performance)
                                                    .where(Performance.competition_id == race_id)
                                                    .where(Performance.user_id == racer_id)).all()
            if len(performance) == 0:
                self.stats[race_id][racer_id] = None
            else:
                self.stats[race_id][racer_id] = performance[0]

class Generator:
    def render(self, racer_id_list, since):
        self.since = since
        loader = Loader(racer_id_list, since)
        stats = loader.stats
        if len(racer_id_list) == 1:
            self.template = env.get_template("1racer.html")
            overview = next(iter(loader.overview.values()))
            return self.render_one(overview, stats, racer_id_list[0])

        else:
            self.template = env.get_template("mulitple_racers.html")    # TODO create template
            overview = loader.overview
            return self.render_multiple(overview, stats)

    def render_one(self, overview, stats, racer_id):
        race_names = list()
        placements = list()
        sliding_medians = list()
        months = [MONTHS_FULL[month] for month in range(NOW.month, 12)] + [MONTHS_FULL[month] for month in range(NOW.month)]
        month_counts = [0 for zero in range(12)]
        order = 0
        for race in stats:
            race_names.append(stats[race]["race_name"])
            performance = stats[race][racer_id]
            if performance is None:
                placements.append(0)    # TODO replace with the value making for no bar in chart
            else:
                placements.append(performance.placement)
                month_counts[race["month"]] += 1
            sliding_medians.append(median(placements[max(0, order-5):]))

            order += 1

        attendances = month_counts[NOW.month+1:] + month_counts[:NOW.month+1]

        print(race_names)
        return self.template.render(name=overview["name"],
                                    participations=overview["participations"],
                                    wins=overview["wins"],
                                    rank=overview["rank"],
                                    date_from=self.since.strftime(DATE_FORMAT),
                                    date_to=NOW.strftime(DATE_FORMAT),
                                    race_names=race_names,
                                    months=months,
                                    placements=placements,
                                    sliding_medians=sliding_medians,
                                    attendances=attendances)

    def render_multiple(self, overview, stats):
        # TODO
        pass

if __name__ == '__main__':
    g = Generator()
    with open('output.html', 'w', encoding='utf-8') as html:
        html.write(g.render([35], since=YEAR_AGO))
        # html.write(g.render(session.testRacer.all()[0]))
