import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from DataLayer.volunteer import Volunteer
from DataLayer.refugee import Refugee
from person_data_retrieve import PersonDataRetrieve
from util import *

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
        if not is_phone_format(phone_num):
           return "Incorrect phone number format"
        
        volunteer_tuples = Volunteer.update_volunteer(id, first_name, last_name, username, password, date_of_birth, phone_num, account_status, camp_id)

        return parse_result('Volunteer', volunteer_tuples)
    
    @staticmethod
    def delete_volunteer(id):
        return Volunteer.delete_volunteer(id)
    
    @staticmethod
    def create_volunteer(id, first_name = None, last_name = None, camp = None, username = None, password = None):
        return UserDataAccess.create_volunteer(first_name, last_name, camp, username, password)
    
    @staticmethod
    def create_refugee(first_name, last_name, camp):
        return UserDataAccess.create_refugee(first_name, last_name, camp)
    
    @staticmethod
    def update_refugee(id, first_name = None, last_name = None):
        refugee = DataAccess.get_refugee_by_id(id)
        if first_name:
            refugee.first_name = first_name
        if last_name:
            refugee.last_name = last_name 
        return UserDataAccess.update_refugee(id, first_name, last_name)
    
    @staticmethod
    def delete_refugee(id):
        return UserDataAccess.delete_refugee(id)
    
