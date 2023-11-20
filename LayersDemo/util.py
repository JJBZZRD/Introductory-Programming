import re

def is_phone_format(phone_num):
    phone_pattern = re.compile(r'^\+\d+$')
    return bool(phone_pattern.match(phone_num))