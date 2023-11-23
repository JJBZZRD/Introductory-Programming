from DataAccessLayer.data_access import DataAccess
from DataAccessLayer.data_access import UserDataAccess
from BusinessLogicLayer.plan_data_validate import ValidatePlan
from datetime import datetime
import random


class PlanEdit:

    @staticmethod
    def generate_plan_id():
        num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        id_plan = ""
        for i in range(6):
            id_plan += str(random.choice(num))
        return int(id_plan)

    @staticmethod
    def create_plan(name, start_date, plan_type, region, event, description):
        # Validation
        for attr in [name, start_date, plan_type, region, event, description]:
            if not attr:
                raise ValueError("Please provide {}".format(attr))

            if not isinstance(attr, str):
                raise ValueError("Please provide the correct input type for {}".format(attr))

        start_date = ValidatePlan.validate_date(start_date, None)
        plan_id = PlanEdit.generate_plan_id()
        return UserDataAccess.create_plan(plan_id, name, start_date, plan_type, region, event, description)

    @staticmethod
    def update_plan(plan_id, name=None, start_date=None, plan_type=None, region=None, event=None, description=None):
        plan = DataAccess.get_plan_by_plan_id(plan_id)

        try:
            name = ValidatePlan.validate_name(name)
            start_date = ValidatePlan.validate_date(start_date, None)
            plan_type = ValidatePlan.validate_plan_type(plan_type)
            region = ValidatePlan.validate_region(region)
            event = ValidatePlan.validate_event(event)
            description = ValidatePlan.validate_description(description)
        except ValueError:
            print("Invalid input")

        if name:
            plan.name = name
        if start_date:
            plan.start_date = start_date
        if plan_type:
            plan.plan_type = plan_type
        if region:
            plan.region = region
        if event:
            plan.event = event
        if description:
            plan.description = description
        return UserDataAccess.update_plan(plan_id, name, start_date, plan_type, region, event, description)

    @staticmethod
    def end_plan(plan_id, end_date):
        plan = DataAccess.get_plan_by_plan_id(plan_id)
        end_date = ValidatePlan.validate_date(None, end_date)

        if end_date:
            plan.end_date = end_date

            if datetime.today().date() == end_date:
                return PlanEdit.delete_plan(plan_id)

        return UserDataAccess.update_plan(plan_id, end_date)

    @staticmethod
    def delete_plan(plan_id):
        return UserDataAccess.delete_plan(plan_id)
