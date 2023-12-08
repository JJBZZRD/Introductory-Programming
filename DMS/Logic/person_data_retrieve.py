from ..DB.volunteer import Volunteer
from ..DB.refugee import Refugee
from .. import util

class PersonDataRetrieve:

    @staticmethod
    def login(username, password):
        # Validate the user's cre dentials using the UserDataAccess class
        if username == 'admin':
            volunteer_tuples = Volunteer.get_volunteer(username=username, password=password)
        else:
            volunteer_tuples = Volunteer.get_volunteer(username=username, password=password, account_status='Active')
        return util.parse_result('Volunteer', volunteer_tuples)

    @staticmethod
    def get_all_volunteers():
        volunteer_tuples = Volunteer.get_all_volunteers() 
        # returns volunteers in list of tuples 
        # [(1, 'Soran', 'Test', 'aaa', 'bbb', '1/1/2000', 7511975055, 'Active', 1), ...]
        # print(f'volunteer_tuples: {volunteer_tuples}')

        if volunteer_tuples: 
            return util.parse_result('Volunteer', volunteer_tuples)
        else:
            return "There is no volunteer"
    # deprecate, use the version that takes multiple args instead
    # @staticmethod
    # def get_volunteers(filter, value):
    #     if not value:
    #         return "You need to specify the filter name and value"
    #     else:
    #         try:
    #             match filter:
    #                 case "id":
    #                     volunteer_tuples = Volunteer.get_volunteer(volunteerID=value)
    #                 case "name":
    #                     res1 = Volunteer.get_volunteer(first_name=value)
    #                     res2 = Volunteer.get_volunteer(last_name=value)
    #                     return util.parse_results('Volunteer', res1, res2)
    #                 case "camp_id":
    #                     volunteer_tuples = Volunteer.get_volunteer(campID=value)
    #                 case "plan_id":
    #                     volunteer_tuples = Volunteer.get_volunteer(planID=value)
    #                 case "account_status":
    #                     volunteer_tuples = Volunteer.get_volunteer(account_status=value)
    #                 case _:
    #                     return "You need to specify the filter name and value"
    #         except:
    #             return "Invalid inputs for get_volunteers(filter, value)"
        
    #         return util.parse_result('Volunteer', volunteer_tuples)

    
    @staticmethod
    def get_volunteers(volunteerID=None, name=None, username=None, password=None, date_of_birth=None, phone=None, account_status=None, campID=None):
        volunteer_tuples_1 = Volunteer.get_volunteer(volunteerID=volunteerID, first_name=name, username=username,password=password, date_of_birth=date_of_birth, phone=phone, account_status=account_status, campID=campID)
        volunteer_tuples_2 = Volunteer.get_volunteer(volunteerID=volunteerID, last_name=name, username=username,password=password, date_of_birth=date_of_birth, phone=phone, account_status=account_status, campID=campID)
        return util.parse_results('Volunteer', volunteer_tuples_1, volunteer_tuples_2)
        

    @staticmethod
    def get_all_refugees():
        refugee_tuples = Refugee.get_all_refugees() 
        return util.parse_result('Refugee', refugee_tuples)

    # @staticmethod
    # def get_refugees(filter, value):
    #     if not value:
    #         return "You need to specify the filter name and value"
    #     else:
    #         try:
    #             match filter:
    #                 case "id":
    #                     refugees = Refugee.get_refugee(refugeeID=value)
    #                 case "name":
    #                     res1 = Refugee.get_refugee(first_name=value)
    #                     res2 = Refugee.get_refugee(last_name=value)
    #                     return util.parse_results('Refugee', res1, res2)
    #                 case "camp_id":
    #                     refugee_tuples = Refugee.get_refugee(campID=value)
    #                 case "plan_id":
    #                     refugee_tuples = Refugee.get_refugee(planID=value)
    #                 case "account_status":
    #                     refugee_tuples = Refugee.get_refugee(account_status=value)
    #                 case "family_id":
    #                     refugee_tuples = Refugee.get_refugee(familyID=value)
    #                 case "medical_condition":
    #                     refugee_tuples = Refugee.get_refugee(medical_condition=value)
    #                 case _:
    #                     return "You need to specify the filter name and value"
    #         except:
    #             return "Invalid inputs for get_refugees(filter, value)"
        
    #         return util.parse_result('Refugee', refugee_tuples)

    @staticmethod
    def get_refugees(id=None, name=None, date_of_birth=None, family_id=None, camp_id=None, medical_condition=None):
        refugee_tuple_1 = Refugee.get_refugee(refugeeID=id, first_name=name, date_of_birth=date_of_birth, familyID=family_id, campID=camp_id, medical_condition=medical_condition)
        refugee_tuple_2 = Refugee.get_refugee(refugeeID=id, last_name=name, date_of_birth=date_of_birth, familyID=family_id, campID=camp_id, medical_conditions=medical_condition)
        return util.parse_results('Refugee', refugee_tuple_1, refugee_tuple_2)