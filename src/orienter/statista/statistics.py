from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime, timedelta
from html import unescape
from numpy import median
from ..databasor import session
from ..databasor.models import *
from ..commander.utils import DATE_FORMAT, MONTHS_FULL
from ..commander.utils import API

NOW = datetime.now()
YEAR_AGO = NOW - timedelta(days=365)

env = Environment(
    loader=PackageLoader('orienter.statista'),
    autoescape=select_autoescape()
)

class Loader:
    def __init__(self, racer_names_list, since):
        self.overview = {racer_name_tuple: dict() for racer_name_tuple in racer_names_list}
        self.stats = dict()
        self.since = since

        for racer_name_t in racer_names_list:
            self.overview[racer_name_t]["participations"] = 0
            self.overview[racer_name_t]["wins"] = 0
            self.overview[racer_name_t]["rank"] = "???"  # TODO replace the DUMMY value with something meaningful

        # temp_racers_that_participated = dict()

        all_races = API.competitions(YEAR_AGO, NOW)
        for race in all_races:
            self.stats[race["id"]] = dict()
            self.stats[race["id"]]["race_name"] = unescape(race["title_sk"])
            self.stats[race["id"]]["month"] = datetime.strptime(race["date_from"], "%Y-%m-%d").month
            for event in race["events"]:
                race_results = API.event_results(race["id"], event["id"])
                for performance in race_results:
                    racer_name_tuple = (performance["first_name"], performance["surname"])

                    # if racer_name_tuple in temp_racers_that_participated:
                    #     temp_racers_that_participated[racer_name_tuple] += 1
                    # else:
                    #     temp_racers_that_participated[racer_name_tuple] = 1

                    if racer_name_tuple in racer_names_list:
                        self.overview[racer_name_tuple]["participations"] += 1
                        if performance["place"] == "1":
                            self.overview[racer_name_tuple]["wins"] += 1
                        self.stats[race["id"]][racer_name_tuple] = performance
            for racer_name_t in racer_names_list:
                if racer_name_t not in self.stats[race["id"]]:
                    self.stats[race["id"]][racer_name_t] = None

        # temp_most_participating_racers = dict(sorted(temp_racers_that_participated.items(), key=lambda item: item[1]))
        #
        # for key, value in temp_most_participating_racers.items():
        #     print(f"{key}: {value}")    # printed reversed so that top values are seen at the bottom of the console

class Generator:
    def render(self, racer_names_list, since):
        self.since = since
        loader = Loader(racer_names_list, since)
        stats = loader.stats
        if len(racer_names_list) == 1:
            self.template = env.get_template("1racer.html")
            overview = next(iter(loader.overview.values()))
            return self.render_one(overview, stats, racer_names_list[0])

        else:
            self.template = env.get_template("mulitple_racers.html")    # TODO create template
            overview = loader.overview
            return self.render_multiple(overview, stats)

    def render_one(self, overview, stats, racer_name_tuple):
        race_names = list()
        placements = list()
        sliding_medians = list()
        months = [MONTHS_FULL[month] for month in range(NOW.month, 12)] + [MONTHS_FULL[month] for month in range(NOW.month)]
        month_counts = [0] * 12
        for order, race in enumerate(stats):
            race_names.append(stats[race]["race_name"])
            performance = stats[race][racer_name_tuple]
            if performance is None:
                placements.append(0)    # TODO replace with the value making for no bar in chart
            else:
                placements.append(int(performance["place"]))
                month_counts[stats[race]["month"]] += 1
            # print(placements[max(0, order-5):])
            sliding_medians.append(median(placements[max(0, order-5):]))

        attendances = month_counts[NOW.month+1:] + month_counts[:NOW.month+1]

        return self.template.render(name=f"{racer_name_tuple[0]} {racer_name_tuple[1]}",
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
        html.write(g.render([("Andrea", "Papugová")], since=YEAR_AGO))
