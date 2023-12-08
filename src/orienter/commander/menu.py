import inspect
import random
import string
from importlib.metadata import version, PackageNotFoundError
from os import environ
from pathlib import Path

from simple_term_menu import TerminalMenu

from .utils import MONTHS_FULL
from .utils import get_races_in_month, get_clubs
from ..communicator import api
from ..configurator import configuration
from ..databasor import models
from ..databasor import session


class Menu:
    API = api.API(configuration.API_KEY, configuration.API_ENDPOINT)

    @staticmethod
    def main_menu():
        try:
            orienter_version = version('orienter')
        except PackageNotFoundError:
            orienter_version = "0.0.0"

        options = ["Pridanie nových pretekov", "Prihlasovanie účastníkov", "Štatistiky"]
        menu = TerminalMenu(options, title=f"Orienter v{orienter_version} - Hlavné menu\n"
                                           "(ukončiť pomocou klávesu q)", accept_keys=("enter", "q"))
        selected_option_index = menu.show()
        if menu.chosen_accept_key == 'q':
            return

        submenus = [Menu.add_race_menu, Menu.signup_menu, Menu.statistics_menu]
        submenus[selected_option_index]()

    @staticmethod
    def add_race_menu():
        month_menu = TerminalMenu(MONTHS_FULL, title="(návrat pomocou klávesu q)", accept_keys=("enter", "q"))
        selected_month = month_menu.show() + 1
        if month_menu.chosen_accept_key == 'q':
            Menu.main_menu()
            return

        # TODO: handle empty races
        races = get_races_in_month(selected_month)
        clubs = get_clubs()
        choices = list()
        for race in races:
            for event in race.events:
                choices.append(f"{event.date}, {event.title_sk}, {race.place}, {clubs[race.organizers[0]].name}")
        races_menu = TerminalMenu(choices, title="Vyberte preteky.\n"
                                                 "dátum konania, názov, miesto konania, organizátor\n"
                                                 "(návrat pomocou klávesu q)",
                                  multi_select=True, accept_keys=("enter", "q"))
        selected_races = races_menu.show()
        if races_menu.chosen_accept_key == 'q':
            Menu.add_race_menu()
            return
        print("Selected races:", selected_races)
        # TODO: do stuff with the selection

    @staticmethod
    def signup_menu():
        # TODO: for now only the competitions name is shown
        stmt = session.select(models.Competition).where(models.Competition.is_active == 1)
        active_races_raw = session.session.scalars(stmt)

        # TODO: handle empty races
        choices = [f"{race.date}, {race.name}" for race in active_races_raw]
        races_menu = TerminalMenu(choices, title="Vyberte preteky.\n"
                                                 "dátum konania, názov\n"
                                                 "(návrat pomocou klávesu q)",
                                  multi_select=False, accept_keys=("enter", "q"))
        selected_races = races_menu.show()
        if races_menu.chosen_accept_key == 'q':
            Menu.main_menu()
            return

        # TODO: for now only the competitors name is shown

        stmt = session.select(models.User)
        racers_raw = session.session.scalars(stmt)
        racers = []
        for scalar in racers_raw:
            tmp = []
            for member in inspect.getmembers(scalar):
                if member[0] == "first_name":
                    tmp.append(str(member[1]))
            racers.append(tmp[:])

        # TODO: handle empty racers
        joined_racers = [", ".join(racer) for racer in racers]
        racers_menu = TerminalMenu(joined_racers, title="Vyberte pretekárov.\n"
                                                        "Meno a priezvisko, klubové id, poznámka\n"
                                                        "(návrat pomocou klávesu q)",
                                   multi_select=True, accept_keys=("enter", "q"))
        selected_racers = racers_menu.show()
        if racers_menu.chosen_accept_key == 'q':
            Menu.signup_menu()
            return

        print("Selected racers:", selected_racers)  # TODO: do stuff with the selection

    @staticmethod
    def statistics_menu():
        racers = [
            ["David Krchňavý", "SKS01101", "chory"],
            ["Ondrej Bublavý", "SKS00109", ""],
        ]  # TODO: get real racers instead of example ones
        # TODO: handle empty racers
        joined_racers = [", ".join(racer) for racer in racers]
        racers_menu = TerminalMenu(joined_racers, title="Vyberte pretekárov.\n"
                                                        "Meno a priezvisko, klubové id, poznámka\n"
                                                        "(návrat pomocou klávesu q)",
                                   multi_select=True, accept_keys=("enter", "q"))
        selected_racers = racers_menu.show()
        if racers_menu.chosen_accept_key == 'q':
            Menu.signup_menu()
            return

        print("Selected racers:", selected_racers)  # TODO: do stuff with the selection
        filename = "orienter_" + ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + ".html"
        path = Path(environ["HOME"]) / filename
        chosen_path = input(f"Zadajte názov súboru aj s cestou [{path}]: ")
        path = chosen_path or path

        print("Chosen path:", path)  # TODO: do stuff with the selection


if __name__ == "__main__":
    Menu.main_menu()
