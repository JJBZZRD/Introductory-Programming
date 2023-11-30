import re
import pycountry as pc


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

