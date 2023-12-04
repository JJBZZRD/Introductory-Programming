from DataLayer.plan import Plan
import util
from datetime import datetime


class PlanEdit:

    @staticmethod
    def create_plan(start_date, end_date, name, region, event_name, description):
        for attr in [start_date, end_date, name, region, event_name, description]:
            if not attr:
                raise ValueError("Please provide {}".format(attr))

            if not isinstance(attr, str):
                raise ValueError("Please provide the correct input type for {}".format(attr))

        start_date = util.validate_date(start_date, None)
        return Plan.create_plan(start_date, end_date, name, region, event_name, description)

    @staticmethod
    def update_plan(planID, start_date=None, end_date=None, name=None, region=None, event_name=None, description=None):
        plan = Plan.get_plan(planID)

        try:
            name = util.validate_name(name)
            start_date = util.validate_date(start_date, None)
            end_date = util.validate_date(start_date, end_date)
            region = util.validate_region(region)
            event_name = util.validate_event(event_name)
            description = util.validate_description(description)
        except ValueError:
            print("Invalid input")

        if name:
            plan.name = name
        if start_date:
            plan.start_date = start_date
        if end_date:
            plan.end_date = end_date
        if region:
            plan.region = region
        if event_name:
            plan.event = event_name
        if description:
            plan.description = description
        return Plan.update_plan(planID, start_date, end_date, name, region, event_name, description)

    @staticmethod
    def end_plan(planID, start_date, end_date):
        plan = Plan.get_plan(planID)
        end_date = util.validate_date(start_date, end_date)

        if end_date:
            plan.end_date = end_date

            if datetime.today().date() == end_date:
                return Plan.update_plan(planID, end_date)

    @staticmethod
    def delete_plan(planID):
        return Plan.delete_plan(planID)
