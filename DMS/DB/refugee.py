from .config import conn, cursor
from .camp import Camp


class Refugee:
    def __init__(
        self,
        refugeeID,
        first_name,
        last_name,
        date_of_birth,
        gender,
        familyID,
        campID,
        triage_category,
        medical_conditions,
        vital_status,
        created_time,
    ):
        self.refugeeID = refugeeID
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.familyID = familyID
        self.campID = campID
        self.triage_category = triage_category
        self.medical_conditions = medical_conditions
        self.vital_status = vital_status
        self.age = 0
        self.band = None
        self.created_time = created_time

    @classmethod
    def init_from_tuple(cls, refugee_tuple):
        return cls(*refugee_tuple)

    def display_info(self):
        return [
            str(self.refugeeID),
            str(self.first_name),
            str(self.last_name),
            str(self.date_of_birth),
            str(self.gender),
            str(self.familyID),
            str(self.campID),
            str(self.triage_category),
            str(self.medical_conditions),
            str(self.vital_status),
            self.created_time,
        ]

    @staticmethod
    def get_refugee_by_id(refugeeID):
        cursor.execute("SELECT * FROM refugees WHERE refugeeID = ?", (refugeeID,))
        return [cursor.fetchone()]

    @classmethod
    def create_refugee(cls, refugee_tuple):
        (
            first_name,
            last_name,
            date_of_birth,
            gender,
            familyID,
            campID,
            triage_category,
            medical_conditions,
            vital_status,
            created_time,
        ) = refugee_tuple
        if Refugee.check_campID_exist(campID):
            sql = """
                INSERT INTO refugees (
                first_name, last_name, date_of_birth, gender, familyID, campID, triage_category, medical_conditions, vital_status, created_time) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(
                sql,
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    familyID,
                    campID,
                    triage_category,
                    medical_conditions,
                    vital_status,
                    created_time,
                ),
            )
            conn.commit()
            refugee_id = cursor.execute(
                "SELECT last_insert_rowid() FROM refugees"
            ).fetchone()[0]
            return Refugee.get_refugee_by_id(refugee_id)
        else:
            return "Camp campID does not exist"

    @staticmethod
    def update_refugee(
        refugeeID,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        gender=None,
        familyID=None,
        campID=None,
        triage_category=None,
        medical_conditions=None,
        vital_status=None,
    ):
        query = []
        params = []

        if first_name is not None:
            query.append("first_name = ?")
            params.append(first_name)
        if last_name is not None:
            query.append("last_name = ?")
            params.append(last_name)
        if date_of_birth is not None:
            query.append("date_of_birth = ?")
            params.append(date_of_birth)
        if gender is not None:
            query.append("gender = ?")
            params.append(gender)
        if familyID is not None:
            query.append("familyID = ?")
            params.append(familyID)
        if campID is not None:
            query.append("campID = ?")
            params.append(campID)
        if triage_category is not None:
            query.append("triage_category = ?")
            params.append(triage_category)
        if medical_conditions is not None:
            query.append("medical_conditions = ?")
            params.append(medical_conditions)
        if vital_status is not None:
            query.append("vital_status = ?")
            params.append(vital_status)

        params.append(refugeeID)
        cursor.execute(
            f"""UPDATE refugees SET {', '.join(query)} WHERE refugeeID = ?""", params
        )
        conn.commit()
        return Refugee.get_refugee_by_id(refugeeID)

    @staticmethod
    def delete_refugee(refugeeID):
        cursor.execute("DELETE FROM refugees WHERE refugeeID = ?", (refugeeID,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            # print(f"Refugee {refugeeID} has been deleted")
            return True
        else:
            # print(f"Refugee {refugeeID} has not been deleted")
            return False

    @staticmethod
    def get_refugee(
        refugeeID=None,
        name=None,
        date_of_birth=None,
        gender=None,
        familyID=None,
        campID=None,
        triage_category=None,
        medical_conditions=None,
        vital_status=None,
    ):
        # print(f"refugeeID: {refugeeID}")
        query = "SELECT * FROM refugees WHERE refugeeID IS NOT NULL"

        if refugeeID:
            query += f" AND refugeeID = {refugeeID}"
        if name:
            query += f" AND (first_name LIKE '%{name}%' OR last_name LIKE '%{name}%')"
        if date_of_birth:
            query += f" AND date_of_birth = '{date_of_birth}'"
        if gender:
            query += f" AND gender = '{gender}'"
        if familyID:
            query += f" AND familyID = {familyID}"
        if campID:
            query += f" AND campID = {campID}"
        if triage_category:
            query += f" AND triage_category = '{triage_category}'"
        if medical_conditions:
            query += f" AND medical_conditions LIKE '%{medical_conditions}%'"
        if vital_status:
            query += f" AND vital_status = '{vital_status}'"

        # print(f"query: {query}")
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_all_refugees():
        cursor.execute("SELECT * FROM refugees")
        return cursor.fetchall()

    @staticmethod
    def check_campID_exist(campID):
        camp = Camp.get_camp_by_id(campID)
        if camp is not None:
            return True
        else:
            return False

    @staticmethod
    def get_by_planID(planID):
        q = f"""
            SELECT *
            FROM refugees
            WHERE campID IN
                (SELECT campID
                FROM camps
                WHERE planID = {planID})
            """
        cursor.execute(q)
        return cursor.fetchall()

    @staticmethod
    def get_refugees_by_plan(
        plan_id, triage_category=None, gender=None, vital_status=None
    ):
        q = f"""
            SELECT *
            FROM refugees
            WHERE campID IN
                (SELECT campID
                FROM camps
                WHERE planID = {plan_id})
            AND refugeeID IS NOT NULL
            """

        if triage_category:
            q += f" AND triage_category = '{triage_category}'"
        if gender:
            q += f" AND gender = '{gender}'"
        if vital_status:
            q += f" AND vital_status = '{vital_status}'"

        cursor.execute(q)
        return cursor.fetchall()

    @staticmethod
    def get_plan_triage_stats(plan_id, triage_category):
        q = f"""
            SELECT *
            FROM refugees
            WHERE campID IN
                (SELECT campID
                FROM camps
                WHERE planID = {plan_id}
            AND triage_category = '{triage_category}')
            """
        cursor.execute(q)
        return cursor.fetchall()

    @staticmethod
    def get_family_count():
        q = f"""
            SELECT COUNT(DISTINCT familyID)
            FROM refugees
            """
        cursor.execute(q)
        return cursor.fetchone()
