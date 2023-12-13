import re
from datetime import datetime
from .DB.volunteer import Volunteer
from .DB.refugee import Refugee
from .DB.plan import Plan
from .DB.camp import Camp
from .DB.countries import *

def get_current_time():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def is_phone_format(phone_num):
    # phone_pattern = re.compile(r'^\+\d+$')
    # bool(phone_pattern.match(phone_num))
    phone_num = phone_num.replace('-', '')
    phone_num = phone_num.replace('+', '')
    return phone_num.isdigit() and len(phone_num) < 13

def is_num(value):
    return float(value)

def is_positive(value):
    num = float(value)
    return num > 0

def is_valid_country(value):
    countries = get_all_countries()
    # print(value)
    # print(countries)
    if value in countries:
        return True
    else:
        return False
    
def is_valid_name(name):
    if all((char.isalpha() or char.isspace()) or char == '-' or char == '\'' for char in name):
        return True
    else:
        return False

def parse_result(class_name, query_result):
    r = "Invalid input"
    if not isinstance(query_result, str):
        match class_name:
            case 'Volunteer':
                r = [Volunteer.init_from_tuple(row) for row in query_result]
            case 'Refugee':
                r = [Refugee.init_from_tuple(row) for row in query_result]
            case 'Plan':
                r = [Plan.init_from_tuple(row) for row in query_result]
            case 'Camp':
                r = [Camp.init_from_tuple(row) for row in query_result]
            case _:
                pass
        # for record in r:
        #     record.display_info()
    return r

def parse_results(class_name, query_result_1, query_result_2):
    r = "Invalid input"
    success_1 = not isinstance(query_result_1, str)
    success_2 = not isinstance(query_result_2, str)
    if success_1 and not success_2:
        r = parse_result(class_name, query_result_1)
    elif not success_1 and success_2:
        r = parse_result(class_name, query_result_2)
    elif success_1 and success_2:
        r = parse_result(class_name, query_result_1 + query_result_2)
    return r
    
def validate_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()

        if not 1 <= date.day <= 31:
            return ValueError("Invalid day")
        elif not 1 <= date.month <= 12:
            return ValueError("Invalid month")
        elif not 2023 <= date.year <= 9999:
            return ValueError("Invalid year")
        
        return True
    
    except Exception as e:
        print(e)
        return False

def validate(value, message):
    if not value:
        return "Please provide {}".format(value)
    elif not isinstance(value, str):
        return message
    return value

def validate_end_date(start_time, end_time):
    try:
        start_time = datetime.strptime(start_time, '%Y-%m-%d').date()
        end_time = datetime.strptime(end_time, '%Y-%m-%d').date()
        if start_time < end_time:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False
     

# def validate_end_date(start_time, end_time):
#     try:
#         if not all(isinstance(date, str) for date in [start_time, end_time]):
#             return "Invalid input type"

#         if not start_time or not end_time:
#             return "Please enter date"

#         start_time = datetime.strptime(start_time, '%Y-%m-%d').date()
#         end_time = datetime.strptime(end_time, '%Y-%m-%d').date()

#         for date in [start_time, end_time]:
#             if not 1 <= date.day <= 31:
#                 return ValueError("Invalid day")
#             elif not 1 <= date.month <= 12:
#                 return ValueError("Invalid month")
#             elif not 2023 <= date.year <= 9999:
#                 return ValueError("Invalid year")

#         if start_time > end_time:
#             return ValueError("Invalid. End time must be after start time")

#         return start_time, end_time

#     except ValueError:
#         return "Invalid input"
    


# from datetime import datetime
# s = '2023-01-01'
# e = '2025-01-01'
# start_time = datetime.strptime(s, '%Y-%m-%d').date()
# end_time = datetime.strptime(e, '%Y-%m-%d').date()
# print(start_time < end_time)