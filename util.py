import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import re
from datetime import datetime
from DataLayer.volunteer import Volunteer
from DataLayer.refugee import Refugee

def is_phone_format(phone_num):
    phone_pattern = re.compile(r'^\+\d+$')
    return bool(phone_pattern.match(phone_num))

def is_num(value):
    return float(value)

def is_positive(value):
    num = float(value)
    return num > 0

def parse_result(class_name, query_result):
    r = "Invalid input"
    if not isinstance(query_result, str):
        match class_name:
            case 'Volunteer':
                r = [Volunteer.init_from_tuple(row) for row in query_result]
            case 'Refugee':
                r = [Refugee.init_from_tuple(row) for row in query_result]
            case _:
                pass
        for record in r:
            record.display_info()
    return r
