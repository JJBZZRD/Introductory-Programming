from .. import util
from ..DB.camp import Camp
from ..DB.plan import Plan
from ..DB.refugee import Refugee

class CampDataRetrieve:

    @staticmethod
    def get_all_camps():
        camp_tuples = Camp.get_all_camps()
        return util.parse_result('Camp', camp_tuples)

    @staticmethod
    def get_camp(campID=None, location=None, max_shelter=None, water=None, max_water=None, food=None, max_food=None,
                 medical_supplies=None, max_medical_supplies=None, planID=None):
        # Currently use pycountry as validation, need to be further changed.
        if location:
            if not util.is_country(location):
                return "You should enter a country name for real."

        if max_shelter:
            if util.is_num(max_shelter):
                if not util.is_positive(max_shelter):
                    return "Cannot enter a negative value to max_shelter."
            else:
                return "You should enter a number to max_shelter."

        if water:
            if util.is_num(water):
                if not util.is_positive(water):
                    return "Cannot enter a negative value to water level."
            else:
                return "You should enter a number to water level."

        if max_water:
            if util.is_num(max_water):
                if not util.is_positive(max_water):
                    return "Cannot enter a negative value to max_water."
            else:
                return "You should enter a number to max_water."

        if food:
            if util.is_num(food):
                if not util.is_positive(food):
                    return "Cannot enter a negative value to food level."
            else:
                return "You should enter a number to food level."

        if max_food:
            if util.is_num(max_food):
                if not util.is_positive(max_food):
                    return "Cannot enter a negative value to max_food."
            else:
                return "You should enter a number to max_food."

        if medical_supplies:
            if util.is_num(medical_supplies):
                if not util.is_positive(medical_supplies):
                    return "Cannot enter a negative value to medical_supplies."
            else:
                return "You should enter a number to medical_supplies."

        if max_medical_supplies:
            if util.is_num(max_medical_supplies):
                if not util.is_positive(max_medical_supplies):
                    return "Cannot enter a negative value to max_medical_supplies."
            else:
                return "You should enter a number to max_medical_supplies."

        if planID:
            if util.is_num(planID):
                if not Plan.get_planID(planID):
                    return "Cannot find this planID. Please try again."
            else:
                return "You should enter a number to planID."
        camp_tuples = Camp.get_camp(campID, location, max_shelter, water, max_water, food, max_food,
                                    medical_supplies, max_medical_supplies, planID)
        # add more validation procedure in the future
        return util.parse_result('Camp', camp_tuples)

    @staticmethod
    def get_camp_resources(campID):
        estimation = []
        resources_name = ['water', 'food']
        refugees = Refugee.get_refugee(campID=campID)

        camp = CampDataRetrieve.get_camp(campID=campID)
        camp = camp[0]

        cost = 1
        cost_med = 1
        for refugee in refugees:
            current_date = datetime.now()
            birth_date = datetime.strptime(refugee.date_of_birth, '%Y-%m-%d')
            age = current_date.year - birth_date.year - (
                    (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            if age < 18:
                cost += 1
            elif 18 <= age < 40:
                cost += 2
            else:
                cost += 0.8

            if refugee.medical_condition is not None:
                cost_med += 1

        for resource in resources_name:
            value = getattr(camp, resource)  # value = camp.water
            estimation.append(value // cost)

        medicine = getattr(camp, 'medical_supplies')
        estimation.append(medicine // cost_med)

        return estimation
