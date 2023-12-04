import config
from volunteer import Volunteer
from admin import Admin
from camp import Camp
from plan import Plan
from refugee import Refugee



# Test create
#Camp.create_camp(location="London", max_shelter=50, water=20, max_water=50, food=30, max_food=50, medical_supplies=40,
#              max_medical_supplies=100, planID=1)

# Test insert
#summer = Camp(location="Bristol", max_shelter=23, water=34, max_water=67, food=45, max_food=56, medical_supplies=45,
#              max_medical_supplies=45, planID=2)
#summer.insert_camp()

# Test update
#Camp.update_camp(1, location="Liverpool")

#Volunteer.create_volunteer(first_name="James", last_name="Smith", username="smithy",
                          #password="123", date_of_birth="05/06/1995", phone=23452345,
                          #account_status="Active", campID=1)
#vol1 = Volunteer(first_name="James", last_name="Smith", username="smithy",
#                           password="123", date_of_birth="05/06/1995", phone=23452345,
#                           account_status="Active", campID=1)

#vol1.insert_volunteer()

#print(Volunteer.create_volunteer(first_name="nnn", last_name="nnn", username="nnn", password="password1", date_of_birth="31/01/2000", phone="13424221", campID=1))
#print(Volunteer.get_volunteer(first_name='aaaa'))


#Plan.create_plan(start_date='11/12/2023', end_date='11/12/2024', name='Hi', region='England', event_name='Earthquake', description='description')
#print(Plan.update_plan(2, name="Wally"))

#print(Refugee.create_refugee(first_name='bbb', last_name='bbb', date_of_birth='11/02/2000', familyID=1, campID=1, medical_condition='is dead'))

print(Volunteer.create_volunteer("John", "Smith", "smith", "123", "11/12/2002", "07329839284", 1))



