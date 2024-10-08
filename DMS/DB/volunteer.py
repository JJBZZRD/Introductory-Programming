from .config import conn, cursor
from .camp import Camp


class Volunteer:
    def __init__(
        self,
        volunteerID,
        first_name,
        last_name,
        username,
        password,
        date_of_birth,
        phone,
        account_status,
        campID,
        created_time,
    ):
        self.volunteerID = volunteerID
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.account_status = account_status
        self.campID = campID
        self.created_time = created_time

    @classmethod
    def init_from_tuple(cls, volunteer_tuple):
        return cls(*volunteer_tuple)

    def display_info(self):
        return [
            str(self.volunteerID),
            str(self.first_name),
            str(self.last_name),
            str(self.username),
            str(self.date_of_birth),
            str(self.phone),
            str(self.account_status),
            str(self.campID),
            self.created_time,
        ]

    @staticmethod
    def get_volunteer_by_id(volunteerID):
        cursor.execute("SELECT * FROM volunteers WHERE volunteerID = ?", (volunteerID,))
        return [cursor.fetchone()]

    @classmethod
    def create_volunteer(cls, volunteer_tuple):
        (
            first_name,
            last_name,
            username,
            password,
            date_of_birth,
            phone,
            account_status,
            campID,
            created_time,
        ) = volunteer_tuple
        if Volunteer.check_campID_exist(campID):
            sql = """
                INSERT INTO volunteers (
                first_name, last_name, username, password, date_of_birth, phone, account_status, campID, created_time) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(
                sql,
                (
                    first_name,
                    last_name,
                    username,
                    password,
                    date_of_birth,
                    phone,
                    account_status,
                    campID,
                    created_time,
                ),
            )
            conn.commit()
            volunteer_id = cursor.execute(
                "SELECT last_insert_rowid() FROM volunteers"
            ).fetchone()[0]
            return Volunteer.get_volunteer_by_id(volunteer_id)
        else:
            return "Camp campID does not exist"

    @staticmethod
    def update_volunteer(
        volunteerID,
        first_name=None,
        last_name=None,
        username=None,
        password=None,
        date_of_birth=None,
        phone=None,
        account_status=None,
        campID=None,
        created_time=None,
    ):
        query = []
        params = []

        if first_name is not None:
            query.append("first_name = ?")
            params.append(first_name)
        if last_name is not None:
            query.append("last_name = ?")
            params.append(last_name)
        if username is not None:
            query.append("username = ?")
            params.append(username)
        if password is not None:
            query.append("password = ?")
            params.append(password)
        if date_of_birth is not None:
            query.append("date_of_birth = ?")
            params.append(date_of_birth)
        if phone is not None:
            query.append("phone = ?")
            params.append(phone)
        if account_status is not None:
            query.append("account_status = ?")
            params.append(account_status)
        if campID is not None:
            if Volunteer.check_campID_exist(campID):
                query.append("campID = ?")
                params.append(campID)
            else:
                return "Camp campID does not exist"
        params.append(volunteerID)
        q = f"""UPDATE volunteers SET {', '.join(query)} WHERE volunteerID = ?"""
        # print(f'q: {q}')
        # print(f'params: {params}')
        cursor.execute(q, params)
        conn.commit()
        return Volunteer.get_volunteer_by_id(volunteerID=volunteerID)

    @staticmethod
    def delete_volunteer(volunteerID):
        cursor.execute("DELETE FROM volunteers WHERE volunteerID = ?", (volunteerID,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            return True
            # print(f"Volunteer {volunteerID} has been deleted")
        else:
            return False
            # print(f"Volunteer {volunteerID} has not been deleted")

    @staticmethod
    def get_volunteer(
        volunteerID=None,
        name=None,
        username=None,
        password=None,
        date_of_birth=None,
        phone=None,
        account_status=None,
        campID=None,
        inclue_admin=False,
        created_time=None,
    ):
        if inclue_admin:
            query = "SELECT * FROM volunteers WHERE volunteerID IS NOT NULL"
        else:
            query = "SELECT * FROM volunteers WHERE campID IS NOT NULL"
        if volunteerID:
            query += f" AND volunteerID = {volunteerID}"
        if name:
            query += f" AND (first_name LIKE '%{name}%' OR last_name LIKE '%{name}%')"
        if username:
            query += f" AND username = '{username}'"
        if password:
            query += f" AND password = '{password}'"
        if date_of_birth:
            query += f" AND date_of_birth = '{date_of_birth}'"
        if phone:
            query += f" AND phone = '{phone}'"
        if account_status:
            query += f" AND account_status = '{account_status}'"
        if campID:
            query += f" AND campID = {campID}"

        # print(f"query: {query}")

        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_all_volunteers():
        cursor.execute("SELECT * FROM volunteers WHERE campID IS NOT NULL")
        return cursor.fetchall()

    @staticmethod
    def active_volunteer_usernames():
        sql = "SELECT username FROM volunteers WHERE account_status = 'Active'"
        cursor.execute(sql)
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
            SELECT * FROM volunteers
            WHERE campID IN (
                SELECT campID FROM camps
                WHERE planID = {planID}
            )"""
        cursor.execute(q)
        return cursor.fetchall()
