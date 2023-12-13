from ..DB.volunteer import Volunteer
from ..DB.refugee import Refugee
from .person_data_retrieve import PersonDataRetrieve
from .. import util
from datetime import datetime

class PersonDataEdit:

    @staticmethod
    def update_volunteer(logged_in_user, volunteerID, first_name = None, last_name = None, phone = None, campID = None, username = None, password = None, date_of_birth = None, account_status = None):

        if first_name:
            first_name = first_name.strip()
        if last_name:
            last_name = last_name.strip()
        if phone:
            phone = phone.strip()
            if not util.is_phone_format(phone):
                return "Incorrect phone number format"
        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"
        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        
        volunteer_tuples = Volunteer.update_volunteer(volunteerID, first_name, last_name, username, password, date_of_birth, phone, account_status, campID)

        return util.parse_result('Volunteer', volunteer_tuples)
        #     if campID:
        #         volunteer.campID = campID
        #     if username:
        #         volunteer.username = username
        #     if password:
        #         volunteer.password = password
        #     if date_of_birth:
        #         volunteer.date_of_birth = date_of_birth
        #     if account_status:
        #         volunteer.account_status = account_status 
        # except:
        #     return "Invalid inputs, please check and try again"
        # validate
    
    @staticmethod
    def delete_volunteer(id):
        res = Volunteer.delete_volunteer(id)
        return f"Volunteer {id} has been deleted" if res else f"There is an error when deleting volunteer {id}"
    
    @staticmethod
    def create_volunteer(logged_in_user, first_name = None, last_name = None, campID = None, username = None, password = None, date_of_birth = None, phone = None):


        if phone and not util.is_phone_format(phone):
           return "Incorrect phone number format"

        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"

        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        t = (first_name, last_name, username, password, date_of_birth, phone, campID, now)

        volunteer_tuples = Volunteer.create_volunteer(t)
        # print(volunteer_tuples)
        return util.parse_result('Volunteer', volunteer_tuples)
    
    @staticmethod
    def create_refugee(logged_in_user, first_name, last_name, date_of_birth, gender, family_id, campID, triage_category = 'None', medical_conditions = None, vital_status = 'Alive'):


        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        t = (first_name, last_name, date_of_birth, gender, family_id, campID, triage_category, medical_conditions, vital_status, now)

        refugee_tuples = Refugee.create_refugee(t)
        return util.parse_result('Refugee', refugee_tuples)

    
    @staticmethod
    def update_refugee(logged_in_user, id, first_name = None, last_name = None, date_of_birth = None, gender=None, family_id = None, campID = None, triage_category=None, medical_conditions = None, vital_status = None):
        # print(f"id: {id}")
        refugee = PersonDataRetrieve.get_refugees(id=id)[0]
        try:
            if first_name:
                refugee.first_name = first_name.strip()
            if last_name:
                refugee.last_name = last_name.strip()
            if date_of_birth:
                refugee.date_of_birth = date_of_birth
            if gender:
                refugee.gender = gender
            if campID:
                refugee.campID = campID
            if family_id:
                refugee.familyID = family_id
            if triage_category:
                refugee.triage_category = triage_category
            if medical_conditions:
                refugee.medical_conditions = medical_conditions
            if vital_status:
                refugee.vital_status = vital_status
        except:
            return "Invalid inputs, please check and try again"
        
        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        
        refugee_tupples = Refugee.update_refugee(id, first_name, last_name, date_of_birth, gender, family_id, campID, triage_category, medical_conditions, vital_status)

        return util.parse_result('Refugee', refugee_tupples)
    
    @staticmethod
    def delete_refugee(id):
        res = Refugee.delete_refugee(id)
        # print(f'res: {res}')
        return f"Refugee {id} has been deleted" if res else f"There is an error when deleting refugee {id}"
