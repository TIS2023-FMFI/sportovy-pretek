from consolemenu import *
from consolemenu.items import *
from consolemenu.prompt_utils import *
from datetime import datetime
from .utils import *
from tabulate import tabulate

CLEAR_SCREEN = False
# TODO: add real package version
menu = ConsoleMenu(f"Hlavné menu", "Orienter v1.0.0",
                   exit_option_text="Koniec", clear_screen=CLEAR_SCREEN)
prompt_utils = PromptUtils(menu.screen)


def add_race():
    global prompt_utils
    current_month = month_number_to_str(datetime.now().month - 1)
    user_response = prompt_utils.input(prompt="mesiac konania pretekov", default=current_month).input_string
    while not validate_month_str(user_response):
        user_response = prompt_utils.input(prompt="mesiac konania pretekov", default=current_month).input_string
    # TODO: handle if no races are returned
    races = [
        ["1", "25.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"],
        ["2", "26.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"]
    ]  # TODO: get real races instead of example ones
    prompt_utils.println(tabulate(races, headers=RACES_TABLE_HEADERS, tablefmt='double_grid'))
    user_response = prompt_utils.input(prompt="čísla pretekov oddelené čiarkou", default="vsetky").input_string
    while not validate_multiple_number_input(user_response, max_value=int(races[-1][0])):
        user_response = prompt_utils.input(prompt="čísla pretekov oddelené čiarkou", default="vsetky").input_string
    prompt_utils.println("vybrane preteky:", user_response)
    # TODO: do stuff with the selection


add_race_item = FunctionItem("Pridanie nových pretekov", add_race, menu=menu)
menu.append_item(add_race_item)


def signup_racer():
    global prompt_utils
    prompt_utils.println("Tieto preteky sú aktívne. Vyberte tie, na ktoré chcete prihlásiť používateľov.")
    # TODO: handle if no races are active
    races = [
        ["1", "25.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"],
        ["2", "26.05.2024", "Majstrovstvá Slovenska v OB v šprintových štafetách", "Martin", "ZMT"]
    ]  # TODO: get real races instead of example ones
    prompt_utils.println(tabulate(races, headers=RACES_TABLE_HEADERS, tablefmt='double_grid'))
    user_response = prompt_utils.input(prompt="číslo pretekov", default=races[0][0]).input_string
    while not validate_multiple_number_input(user_response, max_value=int(races[-1][0]), max_numbers=1):
        user_response = prompt_utils.input(prompt="čísla pretekov oddelené čiarkou", default="vsetky").input_string

    prompt_utils.println("Títo pretekári sa prihlásili na zvolené preteky.")
    prompt_utils.println("Zadajte čísla tých, ktorých neprihlásiť.")
    racers = [
        ["1", "David Krchňavý", "SKS01101", "chory"],
        ["2", "Ondrej Bublavý", "SKS00109", ""],
    ]  # TODO: get real racers instead of example ones
    prompt_utils.println(tabulate(racers, headers=RACES_TABLE_HEADERS, tablefmt='double_grid'))
    user_response = prompt_utils.input(prompt="čísla pretekárov oddelené čiarkou", default=races[0][0]).input_string
    while not validate_multiple_number_input(user_response, max_value=int(races[-1][0])):
        user_response = prompt_utils.input(prompt="čísla pretekárov oddelené čiarkou", default=races[0][0]).input_string
    # TODO: do stuff with the selection


signup_racer_item = FunctionItem("Prihlasovanie účastníkov", signup_racer, menu=menu)
menu.append_item(signup_racer_item)

statistics_submenu = SelectionMenu([], exit_option_text="Návrat", clear_screen=CLEAR_SCREEN)
statistics_item = SubmenuItem("Štatistiky", statistics_submenu, menu)
menu.append_item(statistics_item)

menu.show()
