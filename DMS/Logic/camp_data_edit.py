from ..DB.camp import Camp
from ..DB.plan import Plan
from .camp_data_retrieve import CampDataRetrieve
from .. import util


class CampDataEdit:

    @staticmethod
    def update_camp(campID, location=None, max_shelter=None, water=None, max_water=None, food=None, max_food=None,
                    medical_supplies=None, max_medical_supplies=None, planID=None):
        # get variables
        camp = CampDataRetrieve.get_camp(campID=campID)
        if len(camp) >0:
            camp = camp[0]
        else:
            return []
        try:
            if location:
                camp = location
            if max_shelter:
                camp.max_shelter = max_shelter
            if water:
                camp.water = water
            if max_water:
                camp.max_water = max_water
            if food:
                camp.food = food
            if max_food:
                camp.max_food = food
            if medical_supplies:
                camp.medical_supplies = medical_supplies
            if max_medical_supplies:
                camp.max_medical_supplies = max_medical_supplies
            if planID:
                camp.planID = planID
        except:
            return "Invalid inputs, please check and try again"
        # validate
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

        camp_tuple = Camp.update_camp(campID, location, max_shelter, water, max_water, food,
                                       max_food, medical_supplies, max_medical_supplies, planID)

        return util.parse_result('Camp', camp_tuple)

    @staticmethod  # Insert a camp into the database without creating a new instance
    def create_camp(location, max_shelter, water, max_water, food, max_food, medical_supplies,
                    max_medical_supplies, planID):
        camp = (location, max_shelter, water, max_water, food, max_food, medical_supplies,
                max_medical_supplies, planID)
        campID = Camp.create_camp(camp_tuple=camp)
        camp_tuple = [Camp.get_campID(campID)]
        return util.parse_result('Camp', camp_tuple)

    @staticmethod
    def delete_camp(campID):
        return Camp.delete_camp(campID)
