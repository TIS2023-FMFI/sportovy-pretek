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
        self.stats = dict()
        self.since = since

        temp_racers_that_participated = dict()

        all_races = API.competitions(YEAR_AGO, NOW)
        for race in all_races:
            self.stats[race["id"]] = dict()
            self.stats[race["id"]]["race_name"] = unescape(race["title_sk"])
            self.stats[race["id"]]["month"] = datetime.strptime(race["date_from"], "%Y-%m-%d").month
            for event in race["events"]:
                race_results = API.event_results(race["id"], event["id"])
                for performance in race_results:
                    racer_name_tuple = (performance["first_name"], performance["surname"])

                    if racer_name_tuple in temp_racers_that_participated:
                        temp_racers_that_participated[racer_name_tuple] += 1
                    else:
                        temp_racers_that_participated[racer_name_tuple] = 1

                    if racer_name_tuple in racer_names_list and performance["place"] is not None:
                        self.stats[race["id"]][racer_name_tuple] = performance
                        # print(performance["time_min"], performance["time_sec"], performance["place"])
            for racer_name_t in racer_names_list:
                if racer_name_t not in self.stats[race["id"]]:
                    self.stats[race["id"]][racer_name_t] = None

        temp_most_participating_racers = dict(sorted(temp_racers_that_participated.items(), key=lambda item: item[1]))

        for key, value in temp_most_participating_racers.items():
            print(f"{key}: {value}")    # printed reversed so that top values are seen at the bottom of the console

class Generator:
    def render(self, racer_names_list, since):
        self.since = since
        loader = Loader(racer_names_list, since)
        stats = loader.stats
        if len(racer_names_list) == 1:
            self.template = env.get_template("1racer.html")
            return self.render_one(stats, racer_names_list[0])

        else:
            self.template = env.get_template("multipleRacers.html")
            return self.render_multiple(stats, racer_names_list)

    def render_one(self, stats, racer_name_tuple):
        participations = 0
        wins = 0
        race_names = list()
        placements = list()
        sliding_medians = list()
        months = [MONTHS_FULL[month] for month in range(NOW.month, 12)] + [MONTHS_FULL[month] for month in range(NOW.month)]
        month_counts = [0] * 12
        month_wins = [0] * 12
        for order, race in enumerate(stats):
            race_names.append(stats[race]["race_name"])
            performance = stats[race][racer_name_tuple]
            if performance is None:
                placements.append(0)    # value for no bar in chart
            else:
                participations += 1
                place = int(performance["place"])
                if place == 1:
                    wins += 1
                    month_wins[stats[race]["month"]] += 1
                placements.append(place)
                month_counts[stats[race]["month"]] += 1
            sliding_medians.append(median(placements[max(0, order-4):]))

        worst_placement = max(placements)
        for i in range(len(placements)):
            if placements[i] == 0:
                placements[i] = worst_placement * 2
            if sliding_medians[i] == 0:
                sliding_medians[i] = worst_placement * 2
        attendances = month_counts[NOW.month+1:] + month_counts[:NOW.month+1]
        victories = month_wins[NOW.month + 1:] + month_wins[:NOW.month + 1]

        return self.template.render(name=f"{racer_name_tuple[0]} {racer_name_tuple[1]}",
                                    participations=participations,
                                    wins=wins,
                                    date_from=self.since.strftime(DATE_FORMAT),
                                    date_to=NOW.strftime(DATE_FORMAT),
                                    race_names=race_names,
                                    months=months,
                                    placements=placements,
                                    sliding_medians=sliding_medians,
                                    attendances=attendances,
                                    victories=victories,
                                    worst_placement=worst_placement + 1)

    def render_multiple(self, stats, racer_name_tuples):
        racers_count = len(racer_name_tuples)
        participations = [0] * racers_count
        wins = [0] * racers_count
        race_names = list()
        placements = [[] for _ in range(racers_count)]
        sliding_medians = [[] for _ in range(racers_count)]
        times = [[] for _ in range(racers_count)]
        months = [MONTHS_FULL[month] for month in range(NOW.month, 12)] + [MONTHS_FULL[month] for month in
                                                                           range(NOW.month)]
        month_counts = [[0] * 12 for _ in range(racers_count)]
        month_wins = [[0] * 12 for _ in range(racers_count)]
        for race in stats:
            race_names.append(stats[race]["race_name"])

        for racer_order, racer_name_tuple in enumerate(racer_name_tuples):
            for order, race in enumerate(stats):
                performance = stats[race][racer_name_tuple]
                if performance is None:
                    placements[racer_order].append(0)  # value for no bar in chart
                    times[racer_order].append(0)
                else:
                    participations[racer_order] += 1
                    place = int(performance["place"])
                    if place == 1:
                        wins[racer_order] += 1
                        month_wins[racer_order][stats[race]["month"]] += 1
                    placements[racer_order].append(place)
                    month_counts[racer_order][stats[race]["month"]] += 1
                    times[racer_order].append(round(int(performance["time_min"]) + int(performance["time_sec"]) / 60, 2))
                sliding_medians[racer_order].append(median(placements[racer_order][max(0, order - 4):]))

        worst_placement = max(map(max, placements))
        worst_time = max(map(max, times))
        attendances = list()
        victories = list()

        for racer_order in range(racers_count):
            for i in range(len(placements[0])):
                if placements[racer_order][i] == 0:
                    placements[racer_order][i] = worst_placement * 2
                    times[racer_order][i] = worst_time * 2
                if sliding_medians[racer_order][i] == 0:
                    sliding_medians[racer_order][i] = worst_placement * 2
            attendances.append(month_counts[racer_order][NOW.month + 1:] + month_counts[racer_order][:NOW.month + 1])
            victories.append(month_wins[racer_order][NOW.month + 1:] + month_wins[racer_order][:NOW.month + 1])

        print(victories)

        return self.template.render(racers_count=racers_count,
                                    names=[f"{rnt[0]} {rnt[1]}" for rnt in racer_name_tuples],
                                    participations=participations,
                                    wins=wins,
                                    date_from=self.since.strftime(DATE_FORMAT),
                                    date_to=NOW.strftime(DATE_FORMAT),
                                    race_names=race_names,
                                    months=months,
                                    placements=placements,
                                    sliding_medians=sliding_medians,
                                    attendances=attendances,
                                    victories=victories,
                                    times=times,
                                    worst_placement=worst_placement + 1,
                                    worst_time=worst_time * 1.2)



if __name__ == '__main__':
    g = Generator()
    with open('output.html', 'w', encoding='utf-8') as html:
        # html.write(g.render([("Andrea", "Papugová")], since=YEAR_AGO))
        html.write(g.render([("Andrea", "Papugová"),
                             ("Karol", "Janšo"),
                             ("Peter", "Kotuliak"),
                             ("Andrej", "Mikloš"),
                             ("Maria", "Dubynets"),
                             ("Iveta", "Putnovská")], since=YEAR_AGO))
