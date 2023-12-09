from ..DB.plan import Plan
from ..DB.countries import *
from datetime import datetime
from .. import util


class PlanEdit:

    @staticmethod
    def create_plan(name, event_name, country, description, start_date, end_date=None, water=None, food=None, medical_supplies=None, shelter=None):
        for attr in [start_date, name, country, event_name, description]:
            if not attr:
                return "Please provide {}".format(attr)

            if not isinstance(attr, str):
                return "Please provide the correct input type for {}".format(attr)

        if country not in get_all_countries():
            return "Please enter a valid country"

        if not util.validate_date(start_date):
            print(f" =============== plan_data_edit.create_plan() ERROR: Invalid date format for start_date: {start_date} has to be yyyy-mm-dd =========")
            return "Invalid date format for start_date: has to be yyyy-mm-dd"
        if end_date and end_date != "Enter End Date in the format yyyy-mm-dd":
            if not util.validate_end_date(start_date, end_date):
                print(f" =============== plan_data_edit.create_plan() ERROR: Invalid end_date: {end_date} has to be in yyyy-mm-dd and greater than start_date =========")
                return "Invalid date format for start_date: has to be yyyy-mm-dd"
        else:
            end_date = None
        plan_tuple = (start_date, end_date, name, country, event_name, description, water, food, medical_supplies, shelter)

        return Plan.create_plan(plan_tuple)

    @staticmethod
    def update_plan(planID=None, name=None, event_name=None, country=None, description=None, start_date=None, end_date=None, water=None, food=None, shelter=None, medical_supplies=None):

        if name:
            name = util.validate_name(name)
        if country:
            country = util.validate_country(country)
        if event_name:
            event_name = util.validate_event(event_name)
        if description:
            description = util.validate_description(description)
        if start_date:
            start_date = util.validate_date(start_date)

        if end_date:
            end_date = util.validate_end_date(start_date, end_date)
        #     if datetime.today().date() == end_date:
        #         return Plan.delete_plan(planID)
        #     else: 
        #         return Plan.update_plan(planID, start_date, end_date, name, country, event_name, description)
        # else:
        #     end_date = None

        return Plan.update_plan(planID, start_date, end_date, name, country, event_name, description, water, food, shelter, medical_supplies)

    # @staticmethod
    # def end_plan(planID, start_date, end_date):
    #     end_date = util.validate_end_date(start_date, end_date)

    #     if end_date:
    #         if datetime.today().date() == end_date:
    #             return Plan.delete_plan(planID)
    #         else:
    #             return Plan.update_plan(planID=planID, end_date=end_date)
            
    @staticmethod
    def delete_plan(planID):
        return 'not' not in Plan.delete_plan(planID)
    
    # @staticmethod
    # def plan_status(planID):
    #     plan = Plan.get_plan(planID)
        
    #     if not plan:
    #         return "Plan"

    #     plan_end_date = datetime.strptime(plan[3], '%d%m%Y').date()

    #     if plan_end_date < datetime.now().date():
    #         return False
    #     else:
    #         return True
