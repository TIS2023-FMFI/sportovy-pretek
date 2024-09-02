import calendar
from typing import Sequence, Mapping
from datetime import timedelta

from sqlalchemy import select, insert

from orienter.databasor import models, schemas, pehapezor
from ..communicator.api import API
from ..communicator.objects import *
from ..databasor.session import Session

DATE_FORMAT_WITH_DAY = "%A, %d.%m.%Y"
DATE_FORMAT = "%d.%m.%Y"
MONTHS = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
MONTHS_FULL = [
    "Január",
    "Február",
    "Marec",
    "Apríl",
    "Máj",
    "Jún",
    "Júl",
    "August",
    "September",
    "Október",
    "November",
    "December",
]
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


def get_clubs(api: API) -> Mapping[int, Club]:
    response_obj = api.clubs()
    return {int(obj["id"]): Club.from_obj(obj) for obj in response_obj}


def get_races_in_month(api: API, month: int) -> Sequence[Competition]:
    now = datetime.now()
    date_from = now.replace(year=now.year + 1 if month < now.month else now.year, month=month, day=1)
    date_to = date_from.replace(day=calendar.monthrange(date_from.year, month)[1])
    response_obj = api.competitions(date_from=date_from.strftime("%Y-%m-%d"), date_to=date_to.strftime("%Y-%m-%d"))
    result = [Competition.from_obj(obj) for obj in response_obj]
    return result


def get_active_races() -> Sequence[models.Competition]:
    with Session.begin() as session:
        stmt = (
            select(models.Competition)
            .where(models.Competition.date > datetime.now())
            .where(models.Competition.is_active == 1)
        )
        competition_schema = schemas.CompetitionSchema()
        return [competition_schema.load(obj, session=session) for obj in pehapezor.exec_select(stmt)]


def check_category_exists(category_id: int) -> bool:
    stmt = select(models.Category).where(models.Category.category_id == category_id).limit(1)
    return bool(pehapezor.exec_select(stmt))


def add_categories_for_race(race_id: int, categories: Mapping[int, Category], race_details: CompetitionDetails):
    for race_category in race_details.categories:
        # multiply the id by 1_000_000 to avoid collision with existing data in the database
        # because the column does not have a UNIQUE constraint set on it (which it should have)
        category_id = int(race_category.category_id) * 1_000_000
        category_name = categories[race_category.category_id].name
        if not check_category_exists(category_id):
            stmt = insert(models.Category).values(category_id=category_id, name=category_name)
            pehapezor.exec_query(stmt)
        stmt = insert(models.CompetitionCategory).values(
            competition_id=race_id, category_id=category_id, api_category_id=race_category.id
        )
        pehapezor.exec_query(stmt)


def check_race_exists(race_id: int) -> bool:
    stmt = select(models.Competition).where(models.Competition.competition_id == race_id).limit(1)
    return bool(pehapezor.exec_select(stmt))


def add_race(race: Competition, event: Event):
    race_id = encode_competition_id(int(race.id), int(event.id))
    if check_race_exists(race_id):
        print("Tieto preteky už existujú:", event.date.strftime(DATE_FORMAT_WITH_DAY), event.title_sk, race.place)
        return
    stmt = insert(models.Competition).values(
        competition_id=race_id,
        name=event.title_sk,
        date=event.date,
        is_active=1,
        comment="",
        signup_deadline=event.date - timedelta(days=3),
    )
    pehapezor.exec_query(stmt)
