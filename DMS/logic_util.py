import re
# import pycountry as pc
from datetime import datetime



def is_phone_format(phone_num):
    phone_pattern = re.compile(r'^\+\d+$')
    return bool(phone_pattern.match(phone_num))


def is_num(value):
    return float(value)


def is_positive(value):
    num = float(value)
    return num > 0


def is_country(value):
    countries = [i.name for i in pc.countries]
    if value in countries:
        return True
    else:
        return False

def validate_date(date):
    try:
        date = datetime.strptime(date, '%d%m%Y').date()

        if not 1 <= date.day <= 31:
                return ValueError("Invalid day")
        elif not 1 <= date.month <= 12:
            return ValueError("Invalid month")
        elif not 1 <= date.year <= 9999:
            return ValueError("Invalid year")
        
        return date
    
    except ValueError:
        return "Invalid input"

def validate_end_date(start_time, end_time):
    try:
        if not all(isinstance(date, str) for date in [start_time, end_time]):
            return "Invalid input type"

        if not start_time or not end_time:
            return "Please enter date"

        start_time = datetime.strptime(start_time, '%d%m%Y').date()
        end_time = datetime.strptime(end_time, '%d%m%Y').date()

        for date in [start_time, end_time]:
            if not 1 <= date.day <= 31:
                return ValueError("Invalid day")
            elif not 1 <= date.month <= 12:
                return ValueError("Invalid month")
            elif not 1 <= date.year <= 9999:
                return ValueError("Invalid year")

        if start_time > end_time:
            return ValueError("Invalid. End time must be after start time")

        return start_time, end_time

    except ValueError:
        return "Invalid input"
    
def validate(value, message):
    if not value:
        return "Please provide {}".format(value)
    elif not isinstance(value, str):
        return message
    return value

def validate_name(name: str):
    return validate(name, "Invalid name")

def validate_country(country: str):
    return validate(country, "Invalid region")

def validate_event(event: str):
    return validate(event, "Invalid event")

def validate_description(description: str):
    return validate(description, "Invalid description")
