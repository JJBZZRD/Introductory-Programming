from DataAccessLayer.data_access import DataAccess

class PersonDataRetrieve:

    @staticmethod
    def get_volunteers():
        return DataAccess.get_all_volunteers()

    @staticmethod
    def get_volunteers(filter, value):
        volunteers = []
        try:
            match filter:
                case "name":
                    if value:
                        volunteers = DataAccess.get_volunteers_by_name(value)
                case "camp":
                    volunteers = DataAccess.get_volunteers_by_camp(value)
                case "plan":
                    volunteers = DataAccess.get_volunteers_by_plan(value)
                case _:
                    return "You need to specify the filter name and value"
        except:
            return "Invalid inputs for get_volunteers(filter, value)"
        return volunteers
    
    @staticmethod
    def get_refugees():
        return DataAccess.get_all_refugees()

    @staticmethod
    def get_refugees(filter, value):
        refugees = []
        try:
            match filter:
                case "name":
                    if value:
                        refugees = DataAccess.get_refugees_by_name(value)
                case "camp":
                    refugees = DataAccess.get_refugees_by_camp(value)
                case _:
                    return "You need to specify the filter name and value"
        except:
            return "Invalid input for get_refugees(filter, value)"
        return refugees 
    