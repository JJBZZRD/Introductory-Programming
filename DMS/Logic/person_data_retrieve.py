from ..DB.volunteer import Volunteer
from ..DB.refugee import Refugee
from ..DB.audit_table import AuditTable
from ..DB.camp import Camp
from .. import util


class PersonDataRetrieve:
    @staticmethod
    def login(username, password):
        if username == "admin":
            volunteer_tuples = Volunteer.get_volunteer(
                username=username, password=password, inclue_admin=True
            )
        else:
            volunteer_tuples = Volunteer.get_volunteer(
                username=username, password=password
            )
        if not AuditTable.log_user_login_history(username, util.get_current_time()):
            return "Failed to log user login history"
        return util.parse_result("Volunteer", volunteer_tuples)

    @staticmethod
    def get_all_volunteers():
        volunteer_tuples = Volunteer.get_all_volunteers()
        # returns volunteers in list of tuples
        # [(1, 'Soran', 'Test', 'aaa', 'bbb', '1/1/2000', 7511975055, 'Active', 1), ...]
        # print(f'volunteer_tuples: {volunteer_tuples}')

        if volunteer_tuples:
            return util.parse_result("Volunteer", volunteer_tuples)
        else:
            return "There is no volunteer"

    @staticmethod
    def get_volunteers_by_plan(planID):
        return util.parse_result("Volunteer", Volunteer.get_by_planID(planID))

    @staticmethod
    def get_volunteers(
        volunteerID=None,
        name=None,
        username=None,
        password=None,
        date_of_birth=None,
        phone=None,
        account_status=None,
        campID=None,
        active=None,
        created_time=None,
        planID=None,
    ):
        if active:
            account_status = "Active"
        elif active == None:
            account_status = None
        else:
            account_status = "Inactive"
        volunteer_tuple = Volunteer.get_volunteer(
            volunteerID=volunteerID,
            name=name,
            username=username,
            password=password,
            date_of_birth=date_of_birth,
            phone=phone,
            account_status=account_status,
            campID=campID,
        )
        vol_list = util.parse_result("Volunteer", volunteer_tuple)
        # print(f'vol_list: {len(vol_list)}')
        if planID:
            # print(f'planID: {planID}')
            camps = util.parse_result("Camp", Camp.get_camp(planID=planID))
            camps = [camp.campID for camp in camps]
            vol_list = [vol for vol in vol_list if vol.campID in camps]
            # print(f'vol_list: {len(vol_list)}')
        return vol_list

    @staticmethod
    def get_all_refugees():
        refugee_tuples = Refugee.get_all_refugees()
        return util.parse_result("Refugee", refugee_tuples)

    def get_refugees_by_plan(
        plan_id, triage_category=None, gender=None, vital_status=None
    ):
        return util.parse_result(
            "Refugee",
            Refugee.get_refugees_by_plan(
                plan_id, triage_category, gender, vital_status
            ),
        )

    @staticmethod
    def get_refugees(
        id=None,
        name=None,
        date_of_birth=None,
        gender=None,
        family_id=None,
        camp_id=None,
        triage_category=None,
        medical_condition=None,
        vital_status=None,
        created_time=None,
        planID=None,
    ):
        # print(f"id: {id}")
        if planID:
            return util.parse_result("Refugee", Refugee.get_refugees_by_plan(planID))

        else:
            refugee_tuple = Refugee.get_refugee(
                refugeeID=id,
                name=name,
                date_of_birth=date_of_birth,
                gender=gender,
                familyID=family_id,
                campID=camp_id,
                triage_category=triage_category,
                medical_conditions=medical_condition,
                vital_status=vital_status,
            )
            # print(f'refugee: {refugee_tuple}')

            return util.parse_result("Refugee", refugee_tuple)
