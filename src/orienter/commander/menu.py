import random
import string
from datetime import timedelta
from importlib.metadata import version, PackageNotFoundError
from os import environ
from pathlib import Path

from simple_term_menu import TerminalMenu
from sqlalchemy import select, insert

from .utils import MONTHS_FULL
from .utils import get_races_in_month, get_clubs
from ..databasor import models, session
from ..statista import statistics


class Menu:

    @staticmethod
    # TODO: make this a while loop
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
        races_list = list()
        for i, race in enumerate(races):
            for j, event in enumerate(race.events):
                races_list.append(
                    [i, j, event.date.strftime('%Y-%m-%d'), event.title_sk, race.place, clubs[race.organizers[0]].name])
        choices = [", ".join(race[2:]) for race in races_list]
        races_menu = TerminalMenu(choices, title="Vyberte preteky.\n"
                                                 "dátum konania, názov, miesto konania, organizátor\n"
                                                 "(návrat pomocou klávesu q)",
                                  multi_select=True, accept_keys=("enter", "q"))
        selected_races = races_menu.show()
        if races_menu.chosen_accept_key == 'q':
            Menu.add_race_menu()
            return
        for selected_race in selected_races:
            race = races[races_list[selected_race][0]]
            event = race.events[races_list[selected_race][1]]
            stmt = select(models.Competition).where(models.Competition.competition_id == race.id)
            existing = session.session.scalars(stmt)
            if existing.all():
                print("Tieto preteky už existujú:", choices[selected_race])
                continue
            three_days = timedelta(days=3)
            stmt = insert(models.Competition).values(competition_id=race.id, name=event.title_sk, date=event.date,
                                                     signup_deadline=event.date - three_days, is_active=0, comment="")
            session.session.execute(stmt)
            session.session.commit()
            # TODO: CATEGORIES!!!!

    @staticmethod
    def signup_menu():
        # TODO: for now only the competitions name is shown
        stmt = select(models.Competition).where(models.Competition.is_active == 1)
        active_races_raw = session.session.scalars(stmt)

        choices = [f"{race.date}, {race.name}" for race in active_races_raw]
        if len(choices) == 0:
            print("Nenašli sa žiadne preteky")
            return

        races_menu = TerminalMenu(choices, title="Vyberte preteky.\n"
                                                 "dátum konania, názov\n"
                                                 "(návrat pomocou klávesu q)",
                                  multi_select=False, accept_keys=("enter", "q"))
        selected_races = races_menu.show()
        if races_menu.chosen_accept_key == 'q':
            Menu.main_menu()
            return

        # TODO: for now only the competitors name is shown

        stmt = select(models.User)
        racers_raw = session.session.scalars(stmt)

        joined_racers = [f"{racer.first_name} {racer.last_name}, {racer.user_club_id}, {racer.comment[:20]}" for racer
                         in racers_raw]
        if len(joined_racers) == 0:
            print("Nenašli sa žiadni pretekári")
            return

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
        stmt = session.select(models.User).where(models.User.first_name == ".")
        racers_raw = session.session.scalars(stmt)

        joined_racers = [f"{racer.first_name} {racer.last_name}, {racer.user_club_id}, {racer.comment[:20]}" for racer
                         in racers_raw]
        if len(joined_racers) == 0:
            print("Nenašli sa žiadni pretekári")
            return

        racers_menu = TerminalMenu(joined_racers, title="Vyberte pretekárov.\n"
                                                        "Meno a priezvisko, klubové id, poznámka\n"
                                                        "(návrat pomocou klávesu q)",
                                   multi_select=True, accept_keys=("enter", "q"))
        selected_racers = racers_menu.show()
        if racers_menu.chosen_accept_key == 'q':
            Menu.signup_menu()
            return

        filename = "orienter_" + ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + ".html"
        path = Path(environ["HOME"]) / filename
        chosen_path = input(f"Zadajte názov súboru aj s cestou [{path}]: ")
        path = chosen_path or path

        user_ids = [int(racer.user_id) for racer in selected_racers]
        Menu.generator.render(user_ids)
        user_ids = [int(racer.user_id) for racer in selected_racers]
        generator = statistics.Generator()
        generator.render(user_ids)


if __name__ == "__main__":
    Menu.main_menu()
