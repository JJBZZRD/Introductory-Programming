from .. import util
from ..DB.camp import Camp

class CampDataRetrieve:

    @staticmethod
    def get_all_camps():
        camp_tuples = Camp.get_all_camps()
        return util.parse_result('Camp', camp_tuples)

    @staticmethod
    def get_camp(campID=None, location=None, max_shelter=None, water=None, max_water=None, food=None, max_food=None,
                 medical_supplies=None, max_medical_supplies=None, planID=None):
        camp_tuples = Camp.get_camp(campID, location, max_shelter, water, max_water, food, max_food,
                                    medical_supplies, max_medical_supplies, planID)
        # add more validation procedure in the future
        return util.parse_result('Camp', camp_tuples)
