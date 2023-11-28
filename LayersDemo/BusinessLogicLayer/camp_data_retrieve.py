from DataLayer.camp import Camp


class CampDataRetrieve:

    @staticmethod
    def get_all_camps():
        return Camp.get_all_camps()

    @staticmethod
    def get_camp(filter, attr):
        camp_infor = []
        try:
            match filter:
                case "campID":
                    if attr:
                        camp_infor = Camp.get_campID(attr)
                case "location":
                    camp_infor = Camp.get_camp(location=attr)
                case "max_shelter":
                    camp_infor = Camp.get_camp(max_shelter=attr)
                case "water":
                    camp_infor = Camp.get_camp(water=attr)
                case "max_water":
                    camp_infor = Camp.get_camp(max_water=attr)
                case "food":
                    camp_infor = Camp.get_camp(food=attr)
                case "max_food":
                    camp_infor = Camp.get_camp(max_food=attr)
                case "medical_supplies":
                    camp_infor = Camp.get_camp(medical_supplies=attr)
                case "max_medical_supplies":
                    camp_infor = Camp.get_camp(max_medical_supplies=attr)
                case "planID":
                    camp_infor = Camp.get_camp(planID=attr)
                case _:
                    return "You need to specify the filter name and attribute"
        except:
            return "Invalid inputs for get_camp(filter, value)"
        return camp_infor
