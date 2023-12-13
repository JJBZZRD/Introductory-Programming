from ..DB.volunteer import Volunteer
from ..DB.refugee import Refugee
from ..DB.audit_table import AuditTable
from .. import util

class PersonDataRetrieve:

    @staticmethod
    def login(username, password):
        # Validate the user's cre dentials using the UserDataAccess class
        if username == 'admin':
            volunteer_tuples = Volunteer.get_volunteer(username=username, password=password, inclue_admin=True)
        else:
            volunteer_tuples = Volunteer.get_volunteer(username=username, password=password, account_status='Active')
        if not AuditTable.log_user_login_history(username, util.get_current_time()):
            return "Failed to log user login history"
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

    @staticmethod
    def get_volunteers_by_plan(planID):
        return util.parse_result('Volunteer', Volunteer.get_by_planID(planID))

    @staticmethod
    def get_volunteers(volunteerID=None, name=None, username=None, password=None, date_of_birth=None, phone=None, account_status=None, campID=None, active=None, created_time=None):

        if active:
            account_status = 'Active'
        elif active == None:
            account_status = None
        else:
            account_status = 'Inactive'

        if name:
            volunteer_tuples_1 = Volunteer.get_volunteer(volunteerID=volunteerID, first_name=name, username=username,password=password, date_of_birth=date_of_birth, phone=phone, account_status=account_status, campID=campID)

            volunteer_tuples_2 = Volunteer.get_volunteer(volunteerID=volunteerID, last_name=name, username=username,password=password, date_of_birth=date_of_birth, phone=phone, account_status=account_status, campID=campID)

            return util.parse_results('Volunteer', volunteer_tuples_1, volunteer_tuples_2)
        else:
            volunteer_tuple = Volunteer.get_volunteer(volunteerID=volunteerID, username=username,password=password, date_of_birth=date_of_birth, phone=phone, account_status=account_status, campID=campID)
            return util.parse_result('Volunteer', volunteer_tuple)

    @staticmethod
    def get_all_refugees():
        refugee_tuples = Refugee.get_all_refugees() 
        return util.parse_result('Refugee', refugee_tuples)
    
    def get_refugees_by_plan(plan_id, triage_category = None, gender = None, vital_status=None):
        return util.parse_result('Refugee', Refugee.get_refugees_by_plan(plan_id, triage_category, gender, vital_status))
    
    @staticmethod
    def get_refugees(id=None, name=None, date_of_birth=None, gender=None, family_id=None, camp_id=None, triage_category=None, medical_condition=None, vital_status=None, created_time=None):
        # print(f"id: {id}")
        if name:
            refugee_tuple_1 = Refugee.get_refugee(refugeeID=id, first_name=name, date_of_birth=date_of_birth, gender=gender, familyID=family_id, campID=camp_id, triage_category=triage_category, medical_conditions=medical_condition, vital_status=vital_status)

            refugee_tuple_2 = Refugee.get_refugee(refugeeID=id, last_name=name, date_of_birth=date_of_birth, gender=gender, familyID=family_id, campID=camp_id, triage_category=triage_category, medical_conditions=medical_condition, vital_status=vital_status)

            # print(f'refugee1: {refugee_tuple_1}')
            # print(f'refugee2: {refugee_tuple_2}')

            return util.parse_results('Refugee', refugee_tuple_1, refugee_tuple_2)
        else:
            refugee_tuple = Refugee.get_refugee(refugeeID=id, first_name=None, last_name=None, date_of_birth=date_of_birth, gender=gender, familyID=family_id, campID=camp_id, triage_category=triage_category, medical_conditions=medical_condition, vital_status=vital_status)
            # print(f'refugee: {refugee_tuple}')

            return util.parse_result('Refugee', refugee_tuple)