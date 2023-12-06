import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from DataLayer.volunteer import *
from DataLayer.plan import *
from DataLayer.camp import *
from BusinessLogicLayer.plan_data_edit import PlanEdit

# b = PlanEdit.create_plan("name", "type", "region", "description", "04122023")
# print(b)


# a = Plan.create_plan('2023-12-04', None, 'test Plan', 'test region', 'test event name', 'aaaaaa')
# print(a)


# Volunteer.create_volunteer('Soran', 'Test', 'aaa', 'bbb', '1/1/2000', '07511975055', 'Active', 1)



# Volunteer.get_all_volunteers()