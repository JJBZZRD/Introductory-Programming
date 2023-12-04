import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from LayersDemo.DataLayer.volunteer import *

Volunteer.create_volunteer('Soran', 'Test', 'aaa', 'bbb', '1/1/2000', '07511975055', 'Active', 1)



Volunteer.get_all_volunteers()