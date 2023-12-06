from ..util import *
from ..DataLayer.camp import Camp

class CampDataRetrieve:

    @staticmethod
    def get_all_camps():
        camp_tuples = Camp.get_all_camps()
        return parse_result('Camp', camp_tuples)

    @staticmethod
    def get_camp(filter, value):
        if not value:
            return "You need to specify the filter name and value"
        else:
            try:
                match filter:
                    case "campID":
                        if value:
                            camp_tuples = Camp.get_camp(campID=value)
                    case "location":
                        camp_tuples = Camp.get_camp(location=value)
                    # case "max_shelter":
                    #     camp_infor = Camp.get_camp(max_shelter=attr)
                    # case "water":
                    #     camp_infor = Camp.get_camp(water=attr)
                    # case "max_water":
                    #     camp_infor = Camp.get_camp(max_water=attr)
                    # case "food":
                    #     camp_infor = Camp.get_camp(food=attr)
                    # case "max_food":
                    #     camp_infor = Camp.get_camp(max_food=attr)
                    # case "medical_supplies":
                    #     camp_infor = Camp.get_camp(medical_supplies=attr)
                    # case "max_medical_supplies":
                    #     camp_infor = Camp.get_camp(max_medical_supplies=attr)
                    # case "planID":
                    #     camp_infor = Camp.get_camp(planID=attr)
                    case _:
                        return "You need to specify the filter name and attribute"
            except Exception as e:
                return f"Error: {e}. Invalid inputs for get_camp(filter, value)"

            return parse_result('Camp', camp_tuples)
