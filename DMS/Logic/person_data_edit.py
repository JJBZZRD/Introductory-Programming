from ..DB.volunteer import Volunteer
from ..DB.refugee import Refugee
from .person_data_retrieve import PersonDataRetrieve
from .. import util
from datetime import datetime

class PersonDataEdit:

    @staticmethod
    def update_volunteer(logged_in_user=None, volunteerID=None, first_name = None, last_name = None, phone = None, campID = None, username = None, password = None, date_of_birth = None, account_status = None, created_time = None):

        if first_name:
            first_name = first_name.strip()
        if last_name:
            last_name = last_name.strip()
        if phone:
            phone = phone.strip()
            if not util.is_phone_format(phone):
                return "Incorrect phone number format"
        if first_name and not util.is_valid_name(first_name):
            return "Incorrect first name format"
        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        if password == "Enter Password":
            password = None
        
        if date_of_birth:
            if util.validate_date(date_of_birth):
                year_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date().year
                current_year = datetime.now().year
                if year_of_birth > current_year:
                    return "      Invalid year of birth      "
            if not util.validate_date(date_of_birth):
                return "Invalid date of birth (yyyy-mm-dd)"

        if campID == 'None':
            campID = None
        if username:
            # print(f"volunteerID: {volunteerID}")
            vols = PersonDataRetrieve.get_volunteers(username=username)
            if isinstance(vols, list) and len(vols) > 0 and str(vols[0].volunteerID) != str(volunteerID):
                return "Username already exists"
        try:
            volunteer_tuples = Volunteer.update_volunteer(volunteerID, first_name, last_name, username, password, date_of_birth, phone, account_status, campID)
        except:
            return "Invalid inputs, please check and try again"
        return util.parse_result('Volunteer', volunteer_tuples)

    @staticmethod
    def delete_volunteer(id):
        res = Volunteer.delete_volunteer(id)
        return f"Volunteer {id} has been deleted" if res else f"There is an error when deleting volunteer {id}"
    
    @staticmethod
    def create_volunteer(logged_in_user=None, first_name = None, last_name = None, campID = None, username = None, password = None, date_of_birth = None, phone = None, account_status = None,created_time = None):

        if phone in ["Enter Phone", '', ' ']:
            return "Please enter phone"
        if phone and not util.is_phone_format(phone):
           return "Incorrect phone number format"

        if first_name in ["Enter First Name", '', ' ']:
            return "Please enter first name"
        if first_name and not util.is_valid_name(first_name):
            return "Incorrect first name format"

        if last_name in ["Enter Last Name", '', ' ']:
            return "Please enter last name"
        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"

        if username in ["Enter Username", '', ' ']:
            return "Please enter username"

        if password in ["Enter Password", '', ' ']:
            return "Please enter password"

        if date_of_birth in ["yyyy-mm-dd", '', ' ']:
            return "Please enter date of birth"
        if date_of_birth and date_of_birth not in ["yyyy-mm-dd", '', ' ']:
            if util.validate_date(date_of_birth):
                year_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date().year
                current_year = datetime.now().year
                if year_of_birth > current_year:
                    return "      Invalid year of birth      "
            if not util.validate_date(date_of_birth):
                return "Invalid date of birth (yyyy-mm-dd)"

        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        t = (first_name, last_name, username, password, date_of_birth, phone, account_status,campID, now)

        volunteer_tuples = Volunteer.create_volunteer(t)
        # print(volunteer_tuples)
        return util.parse_result('Volunteer', volunteer_tuples)
    
    @staticmethod
    def create_refugee(logged_in_user=None, first_name=None, last_name=None, date_of_birth=None, gender=None, family_id=None, campID=None, triage_category = 'None', medical_conditions = None, vital_status = 'Alive'):

        if first_name in ["Enter First Name", '', ' ']:
            return "Please enter first name"
        if first_name and not util.is_valid_name(first_name):
            return "Incorrect first name format"

        if last_name in ["Enter Last Name", '', ' ']:
            return "Please enter last name"
        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        
        if date_of_birth in ["yyyy-mm-dd", '', ' ']:
            return "Please enter date of birth"
        if date_of_birth and date_of_birth not in ["yyyy-mm-dd", '', ' ']:
            if util.validate_date(date_of_birth):
                year_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date().year
                current_year = datetime.now().year
                if year_of_birth > current_year:
                    return "      Invalid year of birth      "
            if not util.validate_date(date_of_birth):
                return "Invalid date of birth (yyyy-mm-dd)"

        if family_id in ["Enter Family ID", '', ' ']:
            family_count = Refugee.get_family_count()[0]
            return f"Please enter family ID, if there is no known family for this refugee, please enter {family_count + 1}"
        if family_id:
            if not util.is_num(family_id):
                return "Family ID must be a number"
            
        if medical_conditions in ["Enter Medical Conditions", '', ' ']:
            medical_conditions = None

        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        t = (first_name, last_name, date_of_birth, gender, family_id, campID, triage_category, medical_conditions, vital_status, now)

        refugee_tuples = Refugee.create_refugee(t)
        return util.parse_result('Refugee', refugee_tuples)

    
    @staticmethod
    def update_refugee(logged_in_user=None, id=None, first_name = None, last_name = None, date_of_birth = None, gender=None, family_id = None, campID = None, triage_category=None, medical_conditions = None, vital_status = None, created_time = None):
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
            if family_id in ["Enter Family ID", '', ' ']:
                family_count = Refugee.get_family_count()[0]
                return f"Please enter family ID, if there is no known family for this refugee, please enter {family_count + 1}"
            if family_id:
                if not util.is_num(family_id):
                    return "Family ID must be a number"
                else:
                    refugee.familyID = family_id
            if triage_category:
                refugee.triage_category = triage_category
            if medical_conditions in ["Enter Medical Conditions", '', ' ']:
                refugee.medical_conditions = None
            if medical_conditions:
                refugee.medical_conditions = medical_conditions
            if vital_status:
                refugee.vital_status = vital_status
        except:
            return "Invalid inputs, please check and try again"
        
        if first_name and not util.is_valid_name(first_name):
            return "Incorrect first name format"

        if last_name and not util.is_valid_name(last_name):
            return "Incorrect last name format"
        
        if date_of_birth:
            if util.validate_date(date_of_birth):
                year_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date().year
                current_year = datetime.now().year
                if year_of_birth > current_year:
                    return "      Invalid year of birth      "
            if not util.validate_date(date_of_birth):
                return "Invalid date of birth (yyyy-mm-dd)"
        
        refugee_tupples = Refugee.update_refugee(id, first_name, last_name, date_of_birth, gender, family_id, campID, triage_category, medical_conditions, vital_status)

        return util.parse_result('Refugee', refugee_tupples)
    
    @staticmethod
    def delete_refugee(id):
        res = Refugee.delete_refugee(id)
        # print(f'res: {res}')
        return f"Refugee {id} has been deleted" if res else f"There is an error when deleting refugee {id}"
