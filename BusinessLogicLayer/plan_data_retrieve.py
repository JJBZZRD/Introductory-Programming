from DataLayer.plan import Plan


class PlanDataRetrieve:

    @staticmethod
    def get_plans():
        plans = []
        plan_tuples = Plan.get_all_plans()

        for plan_tuple in plan_tuples:
            plan = Plan(plan_tuple)
            plans.append(plan)

        return plans

    @staticmethod
    def get_plan(filter, value):
        try:
            match filter:
                case "name":
                    if value:
                        plan_tuple = Plan.get_plan(name=value)
                case "start date":
                    plan_tuple = Plan.get_plan(start_date=value)
                case "type":
                    plan_tuple = Plan.get_plan(type=value)
                case "region":
                    plan_tuple = Plan.get_plan(region=value)
                case "id":
                    plan_tuple = Plan.get_plan(planID=value)
                case "event name":
                    plan_tuple = Plan.get_plan(event_name=value)
                case "description":
                    plan_tuple = Plan.get_plan(description=value)
                case _:
                    return "You need to specify the filter name and attribute"
        except:
            return "Invalid inputs for get_plan(filter, value)"
        
        for plan in plan_tuple:
            if type(plan_tuple) is tuple:
                pass
            else:
                return plan_tuple

        plans = []
        for plan in plan_tuple:
            plan_obj = Plan(plan)
            plans.append(plan_obj)

        return plans
