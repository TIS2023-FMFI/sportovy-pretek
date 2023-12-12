import calendar
from datetime import datetime
from typing import List, Dict

from ..communicator import api
from ..communicator.objects import *
from ..configurator import configuration

DATE_FORMAT = '%A, %d.%m. %Y'
MONTHS = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']
MONTHS_FULL = ["Január", "Február", "Marec", "Apríl", "Máj", "Jún",
               "Júl", "August", "September", "Október", "November", "December"]
RACES_TABLE_HEADERS = ["Číslo", "Dátum", "Názov", "Miesto", "Organizátor"]
RACER_TABLE_HEADERS = ["Číslo", "Meno a priezvisko", "Klubové ID", "Poznámka"]


def month_number_to_str(month: int) -> str:
    return MONTHS[month]


def validate_month_str(month: str) -> bool:
    return month in MONTHS


def validate_multiple_number_input(user_input: str, max_value: int = 1_000_000, max_numbers: int = 1_000_000) -> bool:
    if user_input == "vsetky":
        return True
    numbers = user_input.split(",")
    if len(numbers) > max_numbers:
        return False
    for number in numbers:
        if not (number.isnumeric() and 0 < int(number) <= max_value):
            return False
    return True


def encode_competition_id(competition_id: int, event_id: int):
    multiplier = 100_000_000
    if event_id >= multiplier:
        raise ValueError("Event ID too large. GG")
    return competition_id * multiplier + event_id


def decode_competition_id(competition_id: int) -> (int, int):
    return divmod(competition_id, 100_000_000)


API = api.API(configuration.API_KEY, configuration.API_ENDPOINT)


def get_clubs():
    response_obj = API.clubs()
    return {int(obj['id']): Club.from_obj(obj) for obj in response_obj}


def get_races_in_month(month: int):
    now = datetime.now()
    date_from = now.replace(year=now.year + 1 if month < now.month else 0, month=month, day=1)
    date_to = date_from.replace(day=calendar.monthrange(date_from.year, month)[1])
    response_obj = API.competitions(date_from=date_from.strftime('%Y-%m-%d'),
                                    date_to=date_to.strftime('%Y-%m-%d'))
    result: List[Competition] = [Competition.from_obj(obj) for obj in response_obj]
    return result
