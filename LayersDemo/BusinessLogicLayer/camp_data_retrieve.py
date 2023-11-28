from DataAccessLayer.data_access import DataAccess


class CampDataRetrieve:

    @staticmethod
    def get_camps():
        return DataAccess.get_all_camp()

    @staticmethod
    def get_camp(filter, value):
        camp_infor = []
        try:
            match filter:
                case "id":
                    if value:
                        camp_infor = DataAccess.get_camp_by_id(value)
                case "name":
                        camp_infor = DataAccess.get_camp_by_name(value)
                case "volunteer":
                    camp_infor = DataAccess.get_camp_by_volunteer(value)
                case "admin":
                    camp_infor = DataAccess.get_camp_by_admin(value)
                case _:
                    return "You need to specify the filter name and value"
        except:
            return "Invalid inputs for get_camp(filter, value)"
        return camp_infor
