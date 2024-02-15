import random
import string
from datetime import timedelta, datetime
from importlib.metadata import version, PackageNotFoundError
from os import environ
from pathlib import Path

from simple_term_menu import TerminalMenu
from sqlalchemy import select, insert

from .utils import MONTHS_FULL, DATE_FORMAT, get_active_races, add_race
from .utils import get_races_in_month, get_clubs, encode_competition_id, decode_competition_id
from ..communicator.api import API
from ..configurator.config import configuration
from ..databasor import models
from ..databasor import pehapezor, schemas
from ..databasor.session import Session
from ..statista import statistics


class Menu:
    @staticmethod
    def main_menu():
        try:
            orienter_version = version('orienter')
        except PackageNotFoundError:
            orienter_version = "0.0.0"

        options = ["Pridanie nových pretekov", "Prihlasovanie účastníkov", "Štatistiky"]
        menu = TerminalMenu(options, title=f"Orienter v{orienter_version} - Hlavné menu\n"
                                           "(ukončiť pomocou klávesu q)", accept_keys=("enter", "q"))
        while True:
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
            return

        api = API(configuration.API_KEY, configuration.API_ENDPOINT)
        races = get_races_in_month(api, selected_month)
        if not races:
            print("V zvolenom mesiaci sa nekonajú žiadne preteky.")
            return
        clubs = get_clubs(api)
        races_list = list()
        menu_choices = list()
        for i, race in enumerate(races):
            for j, event in enumerate(race.events):
                race_data = [i, j, event.date.strftime(DATE_FORMAT), event.title_sk, race.place,
                             clubs[race.organizers[0]].name]
                races_list.append(race_data)
                menu_choices.append(", ".join(race_data[2:] +
                                              (["POZOR: PRIHLASOVANIE ZATVORENÉ!"] if not race.entries_open else [])))
        races_menu = TerminalMenu(menu_choices, title="Vyberte preteky.\n"
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
            add_race(api, race, event)
            print("Preteky sa úspešne uložili: ", event.date.strftime(DATE_FORMAT), event.title_sk, race.place)

    @staticmethod
    def signup_menu():
        active_races_raw = get_active_races()
        menu_choices = [f"{race.date.strftime(DATE_FORMAT)}, {race.name}" for race in active_races_raw]
        if len(menu_choices) == 0:
            print("Nenašli sa žiadne aktívne preteky.")
            return

        races_menu = TerminalMenu(menu_choices, title="Vyberte preteky.\n"
                                                      "dátum konania, názov\n"
                                                      "(návrat pomocou klávesu q)",
                                  multi_select=False, accept_keys=("enter", "q"))
        selected_race_number = races_menu.show()
        if races_menu.chosen_accept_key == 'q':
            return
        selected_race: models.Competition = active_races_raw[selected_race_number]
        with Session.begin() as session:
            stmt = session.query(models.User, models.Signup) \
                .join(models.Signup, models.Signup.user_id == models.User.user_id) \
                .where(models.Signup.competition_id == selected_race.competition_id)
            racers_raw = pehapezor.exec_select(stmt.statement)

            joined_racers = [
                f"{row['meno']} {row['priezvisko']}, {row['os_i_c']}, {row['poznamka'][:20] or '--'}"
                for row in racers_raw
            ]
            if len(joined_racers) == 0:
                print("Nenašli sa žiadni pretekári prihlásení na tieto preteky.")
                return

            preselected_entries = []
            while True:
                racers_menu = TerminalMenu(joined_racers, title="Vyberte pretekárov.\n"
                                                                "Meno a priezvisko, klubové id, poznámka\n"
                                                                "(invertovať výber pomocou klávesu i, návrat pomocou q)",
                                           multi_select=True, multi_select_select_on_accept=False,
                                           multi_select_empty_ok=True, accept_keys=('enter', 'q', 'i'),
                                           preselected_entries=preselected_entries)
                selected_racers = racers_menu.show()
                if racers_menu.chosen_accept_key == 'q':
                    Menu.signup_menu()
                    return
                elif racers_menu.chosen_accept_key == 'i':
                    preselected_entries = set(range(len(joined_racers))) - set(selected_racers or {})
                elif selected_racers:
                    break

            comp_id, event_id = decode_competition_id(selected_race.competition_id)
            for selected_racer_num in selected_racers:
                selected_racer: models.User = racers_raw[selected_racer_num]
                stmt = session.query(models.Signup, models.CompetitionCategory) \
                    .join(models.CompetitionCategory,
                          (models.Signup.competition_id == models.CompetitionCategory.competition_id) &
                          (models.Signup.category_id == models.CompetitionCategory.category_id)) \
                    .where(models.Signup.competition_id == selected_race.competition_id) \
                    .where(models.Signup.user_id == selected_racer['id'])
                query_result = pehapezor.exec_select(stmt.statement)
                result = query_result[0] if query_result else None
                input_mapping = {
                    "registration_id": "0",
                    "first_name": selected_racer['meno'],
                    "surname": selected_racer['priezvisko'],
                    "reg_number": selected_racer['os_i_c'],
                    "sportident": selected_racer['cip'],
                    "comment": selected_racer['poznamka'],
                    "categories": [
                        {
                            "competition_event_id": event_id,
                            "competition_category_id": result['api_comp_cat_id']
                        }
                    ] if result else []
                }
                api = API(configuration.API_KEY, configuration.API_ENDPOINT)
                response = api.create_registration(comp_id, input_mapping)
                out = f"OK - {selected_racer.first_name} {selected_racer.last_name}, entry_id: {response['entry_id']}" \
                      + f", entry_runner_id: {response['entry_runner_id']}"
                print(out)

    @staticmethod
    def statistics_menu():
        with Session.begin() as session:
            stmt = select(models.User).order_by(models.User.last_name)
            racer_schema = schemas.UserSchema()
            racers_raw = [racer_schema.load(obj, session=session) for obj in pehapezor.exec_select(stmt)]

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
            return

        filename = "orienter_" + ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + ".html"
        path = Path(environ["HOME"]) / filename
        chosen_path = input(f"Zadajte názov súboru aj s cestou [{path}]: ")
        path = chosen_path or path

        user_names = [(racers_raw[racer_col_num].first_name, racers_raw[racer_col_num].last_name) for racer_col_num in
                      selected_racers]
        generator = statistics.Generator()
        with open(path, 'w', encoding='UTF-8') as html:
            html.write(generator.render(user_names, datetime.now() - timedelta(days=365)))


if __name__ == "__main__":
    Menu.main_menu()
