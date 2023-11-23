from DataAccessLayer.data_access import DataAccess


class PlanDataRetrieve:

    @staticmethod
    def get_camp(filter, value):
        plan = []
        match filter:
            case "name":
                if value:
                    plan = DataAccess.get_plan_by_name(value)
            case "type":
                plan = DataAccess.get_plan_by_type(value)
            case "region":
                plan = DataAccess.get_plan_by_region(value)
            case "plan id":
                plan = DataAccess.get_plan_by_plan_id(value)
            case _:
                return "You need to specify the filter name and attribute"
        return plan
