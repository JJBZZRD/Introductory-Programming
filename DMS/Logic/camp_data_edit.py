from ..DB.camp import Camp
from ..DB.plan import Plan
from .camp_data_retrieve import CampDataRetrieve
from .. import util
from datetime import datetime

class CampDataEdit:

    @staticmethod
    def update_camp(logged_in_user=None, campID=None, location=None, shelter=None, water=None,food=None, medical_supplies=None, planID=None, created_time=None):
        # get variables
        camp = CampDataRetrieve.get_camp(campID=campID)
        if len(camp) >0:
            camp = camp[0]
        else:
            return "Cannot find this campID. Please try again."
        
        plan = util.parse_result('Plan', Plan.get_plan_by_id(planID))[0]

        if plan.status != 'Active':
            return "You are not allowed to edit this camp because the plan has ended."

        try:
            if location:
                camp.location = location
            if shelter:
                camp.shelter = shelter
            if water:
                camp.water = water
            if food:
                camp.food = food
            if medical_supplies:
                camp.medical_supplies = medical_supplies
            if planID:
                camp.planID = planID
        except:
            return "Invalid inputs, please check and try again"
        # validate
        if location:
            if not util.is_valid_name(location):
                return "You should enter a valid location name."
        if shelter:
            if util.is_num(shelter):
                if not util.is_positive(shelter):
                    return "Cannot enter a negative value to shelter."
            else:
                return "You should enter a number to shelter."
        if water:
            if util.is_num(water):
                if not util.is_positive(water):
                    return "Cannot enter a negative value to water level."
            else:
                return "You should enter a number to water level."
        if food:
            if util.is_num(food):
                if not util.is_positive(food):
                    return "Cannot enter a negative value to food level."
            else:
                return "You should enter a number to food level."
        if medical_supplies:
            if util.is_num(medical_supplies):
                if not util.is_positive(medical_supplies):
                    return "Cannot enter a negative value to medical_supplies."
            else:
                return "You should enter a number to medical_supplies."
        if planID:
            if util.is_num(planID):
                if len(Plan.get_plan_by_id(planID)) < 1:
                    return "Cannot find this planID. Please try again."

        camp_tuple = Camp.update_camp(campID, location, shelter, water, food,medical_supplies, planID)

        return util.parse_result('Camp', camp_tuple)

    @staticmethod  # Insert a camp into the database without creating a new instance
    def create_camp(logged_in_user=None, location=None, shelter=None, water=None, food=None, medical_supplies=None, planID=None, created_time=None):
                # validate
        if location:
            if not util.is_valid_name(location):
                return "You should enter a valid location name."
        if shelter:
            if util.is_num(shelter):
                if not util.is_positive(shelter):
                    return "Cannot enter a negative value to shelter."
            else:
                return "You should enter a number to shelter."
        if water:
            if util.is_num(water):
                if not util.is_positive(water):
                    return "Cannot enter a negative value to water level."
            else:
                return "You should enter a number to water level."
        if food:
            if util.is_num(food):
                if not util.is_positive(food):
                    return "Cannot enter a negative value to food level."
            else:
                return "You should enter a number to food level."
        if medical_supplies:
            if util.is_num(medical_supplies):
                if not util.is_positive(medical_supplies):
                    return "Cannot enter a negative value to medical_supplies."
            else:
                return "You should enter a number to medical_supplies."
        if planID:
            if util.is_num(planID):
                if len(Plan.get_plan_by_id(planID)) < 1:
                    return "Cannot find this planID. Please try again."
                
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        camp_tuple = (location, shelter, water, food, medical_supplies, planID, now)
            
        camps = Camp.create_camp(camp_tuple)
        return util.parse_result('Camp', camps)

    @staticmethod
    def delete_camp(campID):
        return f"Camp {campID} has been deleted" if Camp.delete_camp(campID) else f"There is an error when deleting camp {campID}"
