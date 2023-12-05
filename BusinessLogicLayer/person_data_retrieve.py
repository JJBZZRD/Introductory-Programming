import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from DataLayer.volunteer import *

class PersonDataRetrieve:

    @staticmethod
    def get_all_volunteers():
        volunteers = []
        volunteer_tuples = Volunteer.get_all_volunteers() 
        #returns volunteers in tuples [(1, 'Soran', 'Test', 'aaa', 'bbb', '1/1/2000', 7511975055, 'Active', 1)] 
        for volunteer_tuple in volunteer_tuples:
            volunteer = Volunteer.init_from_tuple(volunteer_tuple)
            volunteer.display_info()
            volunteers.append(volunteer)

        return volunteers
    
    @staticmethod
    def get_volunteers(filter, value):
        volunteers = []
        try:
            match filter:
                case "name":
                    if value:
                        volunteers = DataAccess.get_volunteers_by_name(value)
                case "camp":
                    if value:
                        volunteers = DataAccess.get_volunteers_by_camp(value)
                case "plan":
                    if value:
                        volunteers = DataAccess.get_volunteers_by_plan(value)
                case _:
                    return "You need to specify the filter name and value"
        except:
            return "Invalid inputs for get_volunteers(filter, value)"
        return volunteers
    
    @staticmethod
    def get_refugees():
        return DataAccess.get_all_refugees()

    @staticmethod
    def get_refugees(filter, value):
        refugees = []
        try:
            match filter:
                case "name":
                    if value:
                        refugees = DataAccess.get_refugees_by_name(value)
                case "camp":
                    if value:
                        refugees = DataAccess.get_refugees_by_camp(value)
                case _:
                    return "You need to specify the filter name and value"
        except:
            return "Invalid input for get_refugees(filter, value)"
        return refugees 
    