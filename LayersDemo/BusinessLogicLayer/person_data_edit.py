from DataAccessLayer.user_data_access import UserDataAccess
from DataAccessLayer.data_access import DataAccess
import util

class PersonDataEdit:

    @staticmethod
    def update_volunteer(id, first_name = None, last_name = None, phone_num = None, camp = None, username = None, password = None):
        # get variables
        volunteer = UserDataAccess.get_volunteer_by_id(id)
        if first_name:
            volunteer.first_name = first_name
        if last_name:
            volunteer.last_name = last_name
        if phone_num:
            volunteer.phone_num = phone_num
        if camp:
            volunteer.camp = camp
        if username:
            volunteer.username = username
        if password:
            volunteer.password = password

        # validate
        if not util.is_phone_format(phone_num):
           return "Incorrect phone number format"
        
        return UserDataAccess.update_volunteer(volunteer)
    
    @staticmethod
    def delete_volunteer(id):
        return UserDataAccess.delete_volunteer(id)
    
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
    
