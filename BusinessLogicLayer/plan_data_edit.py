from DataLayer.plan import Plan
from datetime import datetime
from BusinessLogicLayer import business_logic_util


class PlanEdit:

    @staticmethod
    def create_plan(name, plan_type, region, description, start_date):
        for attr in [name, plan_type, region, description, start_date]:
            if not attr:
                return "Please provide {}".format(attr)

            if not isinstance(attr, str):
                return "Please provide the correct input type for {}".format(attr)

        start_date = business_logic_util.validate_date(start_date)
        return Plan.create_plan(start_date, None, name, region, None, description)

    @staticmethod
    def update_plan(planID, name, plan_type, region, description, start_date):

        name = business_logic_util.validate_name(name)
        plan_type = business_logic_util.validate_plan_type(plan_type)
        # end_date = util.validate_end_date(start_date, end_date)
        region = business_logic_util.validate_region(region)
        # event_name = util.validate_event(event_name)
        description = business_logic_util.validate_description(description)
        start_date = business_logic_util.validate_date(start_date)

        return Plan.update_plan(planID, start_date, None, name, region, None, description)

    @staticmethod
    def end_plan(planID, start_date, end_date):
        end_date = business_logic_util.validate_end_date(start_date, end_date)

        if end_date:
            if datetime.today().date() == end_date:
                return Plan.delete_plan(planID)
            else:
                return Plan.update_plan(planID=planID, end_date=end_date)
            
    @staticmethod
    def delete_plan(planID):
        return Plan.delete_plan(planID)
