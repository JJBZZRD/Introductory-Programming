from DataAccessLayer.data_access import DataAccess


class CampDataRetrieve:

    @staticmethod
    def get_camp():
        return DataAccess.get_all_camp()

    @staticmethod
    def get_camp(filter, attr):
        camp_infor = []
        try:
            match filter:
                case "name":
                    if attr:
                        camp_infor = DataAccess.get_camp_by_name(attr)
                case "volunteer":
                    camp_infor = DataAccess.get_camp_by_volunteer(attr)
                case "admin":
                    camp_infor = DataAccess.get_camp_by_admin(attr)
                case _:
                    return "You need to specify the filter name and attribute"
        except:
            return "Invalid inputs for get_camp(filter, value)"
        return camp_infor
