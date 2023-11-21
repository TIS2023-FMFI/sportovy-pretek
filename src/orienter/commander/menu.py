from consolemenu import *
from consolemenu.items import *
from consolemenu.prompt_utils import *
from datetime import datetime
from .utils import *
from tabulate import tabulate
from importlib.metadata import version, PackageNotFoundError


class Menu:
    def __init__(self):
        self.CLEAR_SCREEN = False
        self.VERSION = None
        try:
            self.VERSION = version('orienter')
        except PackageNotFoundError:
            self.VERSION = "0.0.0"

        self.menu = ConsoleMenu(f"Hlavné menu", f"Orienter v{self.VERSION}",
                                exit_option_text="Koniec", clear_screen=self.CLEAR_SCREEN)
        self.prompt_utils = PromptUtils(self.menu.screen)

        add_race_item = FunctionItem("Pridanie nových pretekov", self.add_race, menu=self.menu)
        self.menu.append_item(add_race_item)

        signup_racer_item = FunctionItem("Prihlasovanie účastníkov", self.signup_racer, menu=self.menu)
        self.menu.append_item(signup_racer_item)

        statistics_submenu = SelectionMenu([], exit_option_text="Návrat", clear_screen=self.CLEAR_SCREEN)
        statistics_item = SubmenuItem("Štatistiky", statistics_submenu, self.menu)
        self.menu.append_item(statistics_item)

    def show(self):
        self.menu.show()

    def add_race(self):
        current_month = month_number_to_str(datetime.now().month - 1)
        user_response = self.prompt_utils.input(prompt="mesiac konania pretekov", default=current_month).input_string
        while not validate_month_str(user_response):
            user_response = self.prompt_utils.input(prompt="mesiac konania pretekov",
                                                    default=current_month).input_string
        races = [
            ["1", "25.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"],
            ["2", "26.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"]
        ]  # TODO: get real races instead of example ones
        if not races:
            self.prompt_utils.println("V zadanom mesiaci sa nekonajú žiadne preteky.")
            return
        self.prompt_utils.println(tabulate(races, headers=RACES_TABLE_HEADERS, tablefmt='double_grid'))
        user_response = self.prompt_utils.input(prompt="čísla pretekov oddelené čiarkou", default="vsetky").input_string
        while not validate_multiple_number_input(user_response, max_value=int(races[-1][0])):
            user_response = self.prompt_utils.input(prompt="čísla pretekov oddelené čiarkou",
                                                    default="vsetky").input_string
        self.prompt_utils.println("vybrane preteky:", user_response)
        # TODO: do stuff with the selection

    def signup_racer(self):
        races = [
            ["1", "25.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"],
            ["2", "26.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"]
        ]  # TODO: get real races instead of example ones
        if not races:
            self.prompt_utils.println("Žiadne preteky nie sú aktívne.")
            return
        self.prompt_utils.println("Tieto preteky sú aktívne. Vyberte tie, na ktoré chcete prihlásiť používateľov.")
        self.prompt_utils.println(tabulate(races, headers=RACES_TABLE_HEADERS, tablefmt='double_grid'))
        user_response = self.prompt_utils.input(prompt="číslo pretekov", default=races[0][0]).input_string
        while not validate_multiple_number_input(user_response, max_value=int(races[-1][0]), max_numbers=1):
            user_response = self.prompt_utils.input(prompt="čísla pretekov oddelené čiarkou",
                                                    default="vsetky").input_string

        self.prompt_utils.println("Títo pretekári sa prihlásili na zvolené preteky.")
        self.prompt_utils.println("Zadajte čísla tých, ktorých neprihlásiť.")
        racers = [
            ["1", "David Krchňavý", "SKS01101", "chory"],
            ["2", "Ondrej Bublavý", "SKS00109", ""],
        ]  # TODO: get real racers instead of example ones
        self.prompt_utils.println(tabulate(racers, headers=RACES_TABLE_HEADERS, tablefmt='double_grid'))
        user_response = self.prompt_utils.input(prompt="čísla pretekárov oddelené čiarkou",
                                                default=races[0][0]).input_string
        while not validate_multiple_number_input(user_response, max_value=int(races[-1][0])):
            user_response = self.prompt_utils.input(prompt="čísla pretekárov oddelené čiarkou",
                                                    default=races[0][0]).input_string
        # TODO: do stuff with the selection
