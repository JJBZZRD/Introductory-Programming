import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from DataLayer.volunteer import *

Volunteer.create_volunteer('Soran', 'Test', 'aaa', 'bbb', '07511975055', 1, 1)