from ..DB.volunteer import Volunteer
from ..DB.refugee import Refugee
from .person_data_retrieve import PersonDataRetrieve
from .. import util
from datetime import datetime

class PersonDataEdit:

    @staticmethod
    def update_volunteer(id, first_name = None, last_name = None, phone_num = None, camp_id = None, username = None, password = None, date_of_birth = None, account_status = None):
        # get variables
        # volunteer = PersonDataRetrieve.get_volunteers('id', id)

        # try:
        #     if first_name:
        #         volunteer.first_name = first_name.strip()
        #     if last_name:
        #         volunteer.last_name = last_name.strip()
        #     if phone_num:
        #         volunteer.phone = phone_num.strip()
        #     if camp_id:
        #         volunteer.campID = camp_id
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
        if phone_num and not util.is_phone_format(phone_num):
           return "Incorrect phone number format"
        print(f'account_status: {account_status}')

        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"
        print(f'account_status: {account_status}')

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        print(f'account_status: {account_status}')
        
        volunteer_tuples = Volunteer.update_volunteer(id, first_name, last_name, username, password, date_of_birth, phone_num, account_status, camp_id)

        return util.parse_result('Volunteer', volunteer_tuples)
    
    @staticmethod
    def delete_volunteer(id):
        res = Volunteer.delete_volunteer(id)
        return f"Volunteer {id} has been deleted" if res else f"There is an error when deleting volunteer {id}"
    
    @staticmethod
    def create_volunteer(first_name = None, last_name = None, camp_id = None, username = None, password = None, date_of_birth = None, phone = None):


        if phone and not util.is_phone_format(phone):
           return "Incorrect phone number format"

        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"

        now = util.get_current_time().strftime("%Y-%m-%dT%H:%M:%S")

        t = (first_name, last_name, username, password, date_of_birth, phone, camp_id, now)

        volunteer_tuples = Volunteer.create_volunteer(t)
        # print(volunteer_tuples)
        return util.parse_result('Volunteer', volunteer_tuples)
    
    @staticmethod
    def create_refugee(first_name, last_name, date_of_birth, gender, family_id, camp_id, triage_category = 'None', medical_conditions = None, vital_status = 'Alive'):


        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"

        now = util.get_current_time().strftime("%Y-%m-%dT%H:%M:%S")

        t = (first_name, last_name, date_of_birth, gender, family_id, camp_id, triage_category, medical_conditions, vital_status, now)
        
        refugee_tuples = Refugee.create_refugee(t)
        return util.parse_result('Refugee', refugee_tuples)

    
    @staticmethod
    def update_refugee(id, first_name = None, last_name = None, date_of_birth = None, family_id = None, camp_id = None, medical_conditions = None):
        refugee = PersonDataRetrieve.get_refugees('id', id)[0]
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
            if medical_conditions:
                refugee.medical_conditions = medical_conditions
        except:
            return "Invalid inputs, please check and try again"
        
        if first_name and not util.is_valid_name(first_name):
            return "Incorrect firt name format"

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        
        refugee_tupples = Refugee.update_refugee(id, first_name, last_name, date_of_birth, family_id, camp_id, medical_conditions)

        return util.parse_result('Refugee', refugee_tupples)
    
    @staticmethod
    def delete_refugee(id):
        res = Refugee.delete_refugee(id)
        # print(f'res: {res}')
        return f"Refugee {id} has been deleted" if res else f"There is an error when deleting refugee {id}"
