MONTHS = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']
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
