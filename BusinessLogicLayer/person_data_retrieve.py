import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from DataLayer.volunteer import Volunteer
from DataLayer.refugee import Refugee
from util import *

class PersonDataRetrieve:

    @staticmethod
    def login(username, password):
        # Validate the user's cre dentials using the UserDataAccess class
        volunteer_tuples = Volunteer.get_volunteer(username=username, password=password)
        volunteers = parse_result('Volunteer', volunteer_tuples)
        return volunteers

    @staticmethod
    def get_all_volunteers():
        volunteer_tuples = Volunteer.get_all_volunteers() 
        # returns volunteers in list of tuples 
        # [(1, 'Soran', 'Test', 'aaa', 'bbb', '1/1/2000', 7511975055, 'Active', 1), ...] 
        volunteers = parse_result(volunteer_tuples)
        return volunteers
    
    @staticmethod
    def get_volunteers(filter, value):
        if not value:
            return "You need to specify the filter name and value"
        else:
            try:
                match filter:
                    case "id":
                        volunteer_tuples = Volunteer.get_volunteer(volunteerID=value)
                    case "name":
                        res1 = Volunteer.get_volunteer(first_name=value)
                        res2 = Volunteer.get_volunteer(last_name=value)
                        return parse_results('Volunteer', res1, res2)
                    case "camp_id":
                        volunteer_tuples = Volunteer.get_volunteer(campID=value)
                    case "plan_id":
                        volunteer_tuples = Volunteer.get_volunteer(planID=value)
                    case "account_status":
                        volunteer_tuples = Volunteer.get_volunteer(account_status=value)
                    case _:
                        return "You need to specify the filter name and value"
            except:
                return "Invalid inputs for get_volunteers(filter, value)"
        
            volunteers = parse_result('Volunteer', volunteer_tuples)

            return volunteers
    
    @staticmethod
    def get_all_refugees():
        refugee_tuples = Refugee.get_all_refugees() 
        refugees = parse_result('Refugee', refugee_tuples)
        return refugees

    @staticmethod
    def get_refugees(filter, value):
        if not value:
            return "You need to specify the filter name and value"
        else:
            try:
                match filter:
                    case "id":
                        refugees = Refugee.get_refugee(refugeeID=value)
                    case "name":
                        res1 = Refugee.get_refugee(first_name=value)
                        res2 = Refugee.get_refugee(last_name=value)
                        return parse_results('Refugee', res1, res2)
                    case "camp_id":
                        refugee_tuples = Refugee.get_refugee(campID=value)
                    case "plan_id":
                        refugee_tuples = Refugee.get_refugee(planID=value)
                    case "account_status":
                        refugee_tuples = Refugee.get_refugee(account_status=value)
                    case "family_id":
                        refugee_tuples = Refugee.get_refugee(familyID=value)
                    case "medical_condition":
                        refugee_tuples = Refugee.get_refugee(medical_condition=value)
                    case _:
                        return "You need to specify the filter name and value"
            except:
                return "Invalid inputs for get_refugees(filter, value)"
        
            refugees = parse_result('Refugee', refugee_tuples)

            return refugees
    