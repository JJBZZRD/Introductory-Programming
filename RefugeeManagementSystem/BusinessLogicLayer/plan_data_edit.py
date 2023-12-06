from DataAccessLayer.data_access import DataAccess
from DataAccessLayer.data_access import UserDataAccess
import util
from datetime import datetime
import random


class PlanEdit:

    @staticmethod
    def create_plan(name, start_date, end_date, plan_type, region, event, description):
        for attr in [name, start_date, plan_type, region, event, description]:
            if not attr:
                raise ValueError("Please provide {}".format(attr))

            if not isinstance(attr, str):
                raise ValueError("Please provide the correct input type for {}".format(attr))

        start_date = util.validate_date(start_date, None)
        return UserDataAccess.create_plan(name, start_date, end_date, plan_type, region, event, description)

    @staticmethod
    def update_plan(plan_id, name=None, start_date=None, end_date=None, plan_type=None, region=None, event=None, description=None):
        plan = DataAccess.get_plan_by_plan_id(plan_id)

        try:
            name = util.validate_name(name)
            start_date = util.validate_date(start_date, None)
            end_date = util.validate_date(start_date, end_date)
            plan_type = util.validate_plan_type(plan_type)
            region = util.validate_region(region)
            event = util.validate_event(event)
            description = util.validate_description(description)
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
    def end_plan(plan_id, start_date, end_date):
        plan = DataAccess.get_plan_by_plan_id(plan_id)
        end_date = util.validate_date(start_date, end_date)

        if end_date:
            plan.end_date = end_date

            if datetime.today().date() == end_date:
                return UserDataAccess.update_plan(plan_id, end_date)

    @staticmethod
    def delete_plan(plan_id):
        return UserDataAccess.delete_plan(plan_id)
