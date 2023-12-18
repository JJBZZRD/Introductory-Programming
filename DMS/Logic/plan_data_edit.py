from ..DB.plan import Plan
from ..DB.countries import *
from datetime import datetime
from .. import util


class PlanEdit:
    @staticmethod
    def check_plan_status():
        plans = util.parse_result("Plan", Plan.get_all_plans())
        for plan in plans:
            if plan.end_date:
                try:
                    plan.end_date_datetime = datetime.strptime(
                        plan.end_date, "%Y-%m-%d"
                    )
                except:
                    plan.end_date_datetime = datetime.strptime(
                        plan.end_date, "%d/%m/%Y"
                    )
            if (
                plan.end_date_datetime > datetime.now()
                or plan.end_date_datetime is None
            ):
                plan.status = "Active"
            else:
                plan.status = "Ended"

    @staticmethod
    def create_plan(
        logged_in_user=None,
        name=None,
        event_name=None,
        country=None,
        description=None,
        start_date=None,
        end_date=None,
        water=None,
        food=None,
        medical_supplies=None,
        shelter=None,
        status="Active",
    ):
        for attr in [start_date, name, country, event_name, description]:
            if not attr:
                return "Please provide {}".format(attr)

            if not isinstance(attr, str):
                return "Please provide the correct input type for {}".format(attr)

        if country not in get_all_countries():
            return "Please enter a valid country"

        if start_date in ["yyyy-mm-dd", "", " "]:
            return "Please enter start date"
        if start_date and start_date not in ["yyyy-mm-dd", "", " "]:
            if not util.validate_date(start_date):
                return "Invalid date for start date (yyyy-mm-dd)"

        if end_date and end_date not in ["yyyy-mm-dd", "", " "]:
            if util.validate_date(end_date):
                if not util.validate_end_date(start_date, end_date):
                    return "Invalid. End date must be after start date"
            if not util.validate_date(end_date):
                return "Invalid date for end date (yyyy-mm-dd)"
        else:
            end_date = None

        if name in ["Enter Plan Name", "", " "]:
            return "Please enter plan name"

        if event_name in ["Enter Event Name", "", " "]:
            return "Please enter event name"

        if description in ["Enter Description", "", " "]:
            return "Please enter description"

        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        plan_tuple = (
            start_date,
            end_date,
            name,
            country,
            event_name,
            description,
            water,
            food,
            medical_supplies,
            shelter,
            status,
            now,
        )

        plan = util.parse_result("Plan", Plan.create_plan(plan_tuple))[0]
        if isinstance(plan, Plan):
            plan.end_date_datetime = (
                datetime.strptime(plan.end_date, "%Y-%m-%d")
                if plan.end_date is not None
                else None
            )
            return plan
        else:
            return util.parse_result("Plan", plan)

    @staticmethod
    def update_plan(
        logged_in_user=None,
        planID=None,
        name=None,
        event_name=None,
        country=None,
        description=None,
        start_date=None,
        end_date=None,
        water=None,
        food=None,
        shelter=None,
        medical_supplies=None,
        status=None,
        created_time=None,
    ):
        tuple = (
            planID,
            start_date,
            end_date,
            name,
            country,
            event_name,
            description,
            water,
            food,
            shelter,
            medical_supplies,
            status,
        )
        # print(f"tuple: {tuple}")

        if status and status not in ["Active", "Ended"]:
            return "Invalid status"
        if status == "Active":
            if country:
                if not util.is_valid_country(country):
                    return "Invalid country"
            if start_date:
                if not util.validate_date(start_date):
                    return "Invalid start date"
            if end_date and end_date != "None":
                if not util.validate_end_date(start_date, end_date):
                    return "Invalid end date"
            # print("aaaaaaaa")
            res = Plan.update_plan(
                planID,
                start_date,
                end_date,
                name,
                country,
                event_name,
                description,
                water,
                food,
                shelter,
                medical_supplies,
                status,
            )

            # print(f"res: Plan.update_plan  {res}")

            return util.parse_result("Plan", res)
        elif status == "Ended":
            if end_date:
                now = datetime.now().date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                if end_date <= now:
                    return "This plan has ended, to re-activate this plan, please update the end date to a future date"
                else:
                    res = Plan.update_plan(
                        planID,
                        start_date,
                        end_date,
                        name,
                        country,
                        event_name,
                        description,
                        water,
                        food,
                        shelter,
                        medical_supplies,
                        "Active",
                    )
                    return util.parse_result("Plan", res)
            else:
                return "Error: ended plan must have an end date"
        else:
            return f"Error: Invalid status: {status}"

    @staticmethod
    def end_plan(planID):
        plan = util.parse_result("Plan", Plan.get_plan(planID))[0]
        if plan:
            plan.end_date = datetime.today().date()
            plan.status = "Ended"
            Plan.update_plan(planID, end_date=plan.end_date, status=plan.status)
            return plan
        else:
            return "Plan does not exist"

    @staticmethod
    def delete_plan(planID):
        return (
            f"Plan {planID} has been deleted"
            if Plan.delete_plan(planID)
            else f"There is an error when deleting plan {planID}"
        )
