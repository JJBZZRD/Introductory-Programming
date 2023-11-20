from DataAccessLayer.user_data_access import UserDataAccess
import util

class PersonDataEdit:


    def update_volunteer(self, id, first_name = None, last_name = None, phone_num = None, camp = None, username = None, password = None):
        # get variables
        volunteer = UserDataAccess.get_volunteer(id)
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
    
    def delete_volunteer(self, id):
        return UserDataAccess.delete_volunteer(id)
    
    def create_volunteer(self, id, first_name = None, last_name = None, camp = None, username = None, password = None):
        return UserDataAccess.create_volunteer(first_name, last_name, camp, username, password)
    
    def create_refugee(self, first_name, last_name, camp):
        return UserDataAccess.create_refugee(first_name, last_name, camp)
    
    def update_refugee(self, id, first_name = None, last_name = None):
        return UserDataAccess.update_refugee(id, first_name, last_name)
    
    def delete_refugee(self, id):
        return UserDataAccess.delete_refugee(id)
    
