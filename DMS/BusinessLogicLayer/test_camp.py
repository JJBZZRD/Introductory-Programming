from camp_data_edit import CampDataEdit
from ..DataLayer.camp import Camp
from ..DataLayer.plan import Plan
from .camp_data_retrieve import CampDataRetrieve
from .. import util


new_plan = Plan.create_plan('2023-12-04', None, 'test Plan', 'test region', 'test event name', 'aaaaaa')

planID = new_plan[0]
print(new_plan)

a = CampDataEdit.create_camp(0, 'Australia', 50, None, 50, None, 50, None, 50, planID)
print(a)

b = CampDataRetrieve.get_all_camps()
print(Camp.get_campID(71))

c = CampDataRetrieve.get_camp("campID", 51)
print(c)




