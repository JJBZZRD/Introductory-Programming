from ..DB.volunteer import Volunteer
from ..DB.refugee import Refugee
from .person_data_retrieve import PersonDataRetrieve
from .. import util

class PersonDataEdit:

    @staticmethod
    def update_volunteer(id, first_name = None, last_name = None, phone_num = None, camp_id = None, username = None, password = None, date_of_birth = None, account_status = None):
        # get variables
        volunteer = PersonDataRetrieve.get_volunteers('id', id)

        try:
            if first_name:
                volunteer.first_name = first_name.strip()
            if last_name:
                volunteer.last_name = last_name.strip()
            if phone_num:
                volunteer.phone = phone_num.strip()
            if camp_id:
                volunteer.campID = camp_id
            if username:
                volunteer.username = username
            if password:
                volunteer.password = password
            if date_of_birth:
                volunteer.date_of_birth = date_of_birth
            if account_status:
                volunteer.account_status = account_status 
        except:
            return "Invalid inputs, please check and try again"
        # validate
        if not util.is_phone_format(phone_num):
           return "Incorrect phone number format"
        
        volunteer_tuples = Volunteer.update_volunteer(id, first_name, last_name, username, password, date_of_birth, phone_num, account_status, camp_id)

        return util.parse_result('Volunteer', volunteer_tuples)
    
    @staticmethod
    def delete_volunteer(id):
        res = Volunteer.delete_volunteer(id)
        return 'not' not in res
    
    @staticmethod
    def create_volunteer(first_name = None, last_name = None, camp_id = None, username = None, password = None, date_of_birth = None, phone = None):
        volunteer_tuples = Volunteer.create_volunteer(first_name, last_name, username, password, date_of_birth, phone, camp_id)
        return util.parse_result('Volunteer', volunteer_tuples)
    
    @staticmethod
    def create_refugee(first_name, last_name, date_of_birth, family_id, camp_id, medical_condition):
        refugee_tuples = Refugee.create_refugee(first_name, last_name, date_of_birth, family_id, camp_id, medical_condition)
        return util.parse_result('Refugee', refugee_tuples)

    
    @staticmethod
    def update_refugee(id, first_name = None, last_name = None, date_of_birth = None, family_id = None, camp_id = None, medical_condition = None):
        refugees = PersonDataRetrieve.get_refugees('id', id)
        refugee = refugees[0]
        try:
            if first_name:
                refugee.first_name = first_name.strip()
            if last_name:
                refugee.last_name = last_name.strip()
            if date_of_birth:
                refugee.date_of_birth = date_of_birth
            if camp_id:
                refugee.campID = camp_id
            if family_id:
                refugee.familyID = family_id
            if medical_condition:
                refugee.medical_condition = medical_condition
        except:
            return "Invalid inputs, please check and try again"
        
        refugee_tupples = Refugee.update_refugee(id, first_name, last_name, date_of_birth, family_id, camp_id, medical_condition)

        return util.parse_result('Refugee', refugee_tupples)
    
    @staticmethod
    def delete_refugee(id):
        res = Refugee.delete_refugee(id)
        return 'not' not in res 
