
import config
from .volunteer import Volunteer
from .plan import Plan



# Test create
#Camp.create_camp(location="London", max_shelter=50, water=20, max_water=50, food=30, max_food=50, medical_supplies=40,
#              max_medical_supplies=100, planID=1)

# Test insert
#summer = Camp(location="Bristol", max_shelter=23, water=34, max_water=67, food=45, max_food=56, medical_supplies=45,
#              max_medical_supplies=45, planID=2)
#summer.insert_camp()

# Test update
#Camp.update_camp(1, location="Liverpool")

#Vol1 = Volunteer(volunteerID = 87, first_name="James", last_name="Smith", username="smithy",
#                          password="123", date_of_birth="05/06/1995", phone=23452345,
#                          account_status="Active", campID=1)
#vol1 = Volunteer(first_name="James", last_name="Smith", username="smithy",
#                           password="123", date_of_birth="05/06/1995", phone=23452345,
#                           account_status="Active", campID=1)

#vol1.insert_volunteer()


plan4_tuple = ("05/07/2024", "05/07/2024", "Monkey Rampage", "Bristol", "Monkey Rampage in Bristol", "Monkeys are rampaging through Bristol")

Plan.create_plan(plan4_tuple)

plan_search_test = Plan.get_plan(name="Mon")
print(plan_search_test)
