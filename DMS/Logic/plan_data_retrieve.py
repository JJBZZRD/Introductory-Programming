from ..DB.plan import Plan
from .. import util


class PlanDataRetrieve:

    @staticmethod
    def get_plans():
        plan_tuples = Plan.get_all_plans()
        return util.parse_result('Plan', plan_tuples)

    @staticmethod
    def get_plan(filter, value):
        if not value:
            return "You need to specify the filter name and value"
        else:
            try:
                match filter:
                    case "id":
                        plan_tuples = Plan.get_plan(planID=value)
                    case "name":
                        plan_tuples = Plan.get_plan(name=value)
                    case "start date":
                        plan_tuples = Plan.get_plan(start_date=value)
                    case "type":
                        plan_tuples = Plan.get_plan(type=value)
                    case "region":
                        plan_tuples = Plan.get_plan(region=value)
                    case "event name":
                        plan_tuples = Plan.get_plan(event_name=value)
                    case "description":
                        plan_tuples = Plan.get_plan(description=value)
            except:
                return "Invalid inputs for get_plan(filter, value)"
            
        return util.parse_result('Plan', plan_tuples)
