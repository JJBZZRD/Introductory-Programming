from DataAccessLayer.user_data_access import UserDataAccess
from DataAccessLayer.data_access import DataAccess
import util

class CampDataEdit:

    @staticmethod
    def undate_camp_name(name, new_name):
        camp = UserDataAccess.get_camp_by_name(name)
        if new_name:
            camp.name = new_name
        # validate
        if util.is_num(new_name):
            return "You should enter a string to camp name."
        return DataAccess.update_camp(camp)

    @staticmethod
    def update_camp(name, volunteer = None, capacity = None, shelters = None, food = None, water = None, medical = None, other = None):
        # get variables
        camp = UserDataAccess.get_camp_by_name(name)
        if volunteer:
            camp.volunteer = volunteer
        if capacity:
            camp.capacity = capacity
        if shelters:
            camp.shelters = shelters
        if food:
            volunteer.camp = food
        if water:
            volunteer.username = water
        if medical:
            volunteer.password = medical
        if other:
            volunteer.other = other

        # validate
        if util.is_num(volunteer):
            return "You should enter a string to volunteer."

        if util.is_num(capacity):
            if not util.is_positive(capacity):
                return "Cannot enter a negative value to capacity of new refugees."
        else:
            return "You should enter a number to volunteer."

        if util.is_num(shelters):
            if not util.is_positive(shelters):
                return "Cannot enter a negative value to shelters."
        else:
            return "You should enter a number to shelters."

        if util.is_num(food):
            if not util.is_positive(food):
                return "Cannot enter a negative value to food level."
        else:
            return "You should enter a number to food level."

        if util.is_num(water):
            if not util.is_positive(water):
                return "Cannot enter a negative value to water level."
        else:
            return "You should enter a number to water level."

        if util.is_num(medical):
            if not util.is_positive(medical):
                return "Cannot enter a negative value to medical level."
        else:
            return "You should enter a number to medical level."

        if util.is_num(other):
            if not util.is_positive(other):
                return "Cannot enter a negative value to ..."
        else:
            return "You should enter a number to ..."

        return DataAccess.update_camp(camp)

