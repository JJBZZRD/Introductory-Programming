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
        plan = []
        try:
            match filter:
                case "name":
                    if value:
                        plan = Plan.get_plan(name=value)
                case "start date":
                    plan = Plan.get_plan(start_date=value)
                case "type":
                    plan = Plan.get_plan(type=value)
                case "region":
                    plan = Plan.get_plan(region=value)
                case "id":
                    plan = Plan.get_plan(planID=value)
                case "event name":
                    plan = Plan.get_plan(event_name=value)
                case "description":
                    plan = Plan.get_plan(description=value)
                case _:
                    return "You need to specify the filter name and attribute"
        except:
            return "Invalid inputs for get_plan(filter, value)"
        return plan
