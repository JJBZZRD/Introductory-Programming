from DataAccessLayer.data_access import DataAccess


class PlanDataRetrieve:

    @staticmethod
    def get_plans():
        return DataAccess.get_all_plan()

    @staticmethod
    def get_plan(filter, value):
        plan = []
        try:
            match filter:
                case "name":
                    if value:
                        plan = DataAccess.get_plan_by_name(value)
                case "type":
                    plan = DataAccess.get_plan_by_type(value)
                case "region":
                    plan = DataAccess.get_plan_by_region(value)
                case "id":
                    plan = DataAccess.get_plan_by_plan_id(value)
                case "event":
                    plan = DataAccess.get_plan_by_event_name(value)
                case "description":
                    plan = DataAccess.get_plan_by_description(value)
                case _:
                    return "You need to specify the filter name and attribute"
        except:
            return "Invalid inputs for get_plan(filter, value)"
        return plan
