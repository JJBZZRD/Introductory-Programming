from plan import Plan
from datetime import datetime
import logic_util


class PlanEdit:

    @staticmethod
    def create_plan(name, event_name, country, description, start_date, end_date=None):
        for attr in [name, event_name, country, description, start_date]:
            if not attr:
                return "Please provide {}".format(attr)

            if not isinstance(attr, str):
                return "Please provide the correct input type for {}".format(attr)

        start_date = logic_util.validate_date(start_date)
        end_date = logic_util.validate_end_date(start_date, end_date)

        plan_tuple = (start_date, end_date, name, country, event_name, description)

        return Plan.create_plan(plan_tuple)

    @staticmethod
    def update_plan(planID, name, event_name, country, description, start_date, end_date):

        name = logic_util.validate_name(name)
        country = logic_util.validate_country(country)
        event_name = logic_util.validate_event(event_name)
        description = logic_util.validate_description(description)
        start_date = logic_util.validate_date(start_date)

        if end_date:
            end_date = logic_util.validate_end_date(start_date, end_date)
            if datetime.today().date() == end_date:
                return Plan.delete_plan(planID)
            else: 
                return Plan.update_plan(planID, start_date, end_date, name, country, event_name, description)
        else:
            end_date = None

        return Plan.update_plan(planID, start_date, end_date, name, country, event_name, description)

    # @staticmethod
    # def end_plan(planID, start_date, end_date):
    #     end_date = logic_util.validate_end_date(start_date, end_date)

    #     if end_date:
    #         if datetime.today().date() == end_date:
    #             return Plan.delete_plan(planID)
    #         else:
    #             return Plan.update_plan(planID=planID, end_date=end_date)
            
    @staticmethod
    def delete_plan(planID):
        return Plan.delete_plan(planID)
    
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
