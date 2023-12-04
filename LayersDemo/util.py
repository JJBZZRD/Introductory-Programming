import re
from datetime import datetime

def is_phone_format(phone_num):
    phone_pattern = re.compile(r'^\+\d+$')
    return bool(phone_pattern.match(phone_num))

def is_num(value):
    return float(value)

def is_positive(value):
    num = float(value)
    return num > 0


