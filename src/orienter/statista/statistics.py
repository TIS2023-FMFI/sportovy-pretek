from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('orienter.statista'),
    autoescape=select_autoescape()
)


class Generator:
    def __init__(self):
        self.template = env.get_template("1racer.html")