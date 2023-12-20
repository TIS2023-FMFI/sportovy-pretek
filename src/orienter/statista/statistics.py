from jinja2 import Environment, PackageLoader, select_autoescape
from ..databasor import session
from ..databasor.models import *

env = Environment(
    loader=PackageLoader('orienter.statista'),
    autoescape=select_autoescape()
)

class Loader:
    def __init__(self, racer_id_list):
        self.overview = dict()
        for id in racer_id_list:
            self.load_one(id)
    def load_one(self, racer_id):
        self.overview[racer_id] = dict()
        racer = session.session.scalars(session.select(User).where(User.user_id == racer_id)).one_or_none()
        racer_name = f"{racer.first_name} {racer.last_name}"
        participations = session.session.scalars(session.select(Signup).where(Signup.user_id == racer_id)).all()
        wins = session.session.scalars(session.select(Performance).where(Performance.user_id == racer_id)
                                       .where(Performance.winner_name == racer_name)).all()
        self.overview[racer_id]["name"] = racer_name
        self.overview[racer_id]["participations"] = len(participations)
        self.overview[racer_id]["wins"] = len(wins)
        self.overview[racer_id]["rank"] = 12345  # TODO replace the DUMMY value with something meaningful




class Generator:
    def render(self, racer_id_list):
        loader = Loader(racer_id_list)
        if len(racer_id_list) == 1:
            self.template = env.get_template("1racer.html")
            overview = next(iter(loader.overview.values()))
            stats = None    # TODO
            return self.render_one(overview, stats)

        else:
            self.template = env.get_template("mulitple_racers.html")    # TODO create template
            overview = loader.overview
            stats = None    # TODO
            return self.render_multiple(overview, stats)

    def render_one(self, overview, stats):
        return self.template.render(name=overview["name"],
                               participations=overview["participations"],
                               wins=overview["wins"],
                               rank=overview["rank"])

    def render_multiple(self, overview, stats):
        # TODO
        pass

if __name__ == '__main__':
    g = Generator()
    with open('output.html', 'w', encoding='utf-8') as html:
        html.write(g.render([1]))
        # html.write(g.render(session.testRacer.all()[0]))
