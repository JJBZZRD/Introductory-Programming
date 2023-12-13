from .config import conn, cursor
from .camp import Camp


class Volunteer:
    def __init__(self, volunteerID, first_name, last_name, username, password, date_of_birth, phone, account_status, campID, created_time):
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
        return [str(self.volunteerID), str(self.first_name), str(self.last_name), str(self.username),
                str(self.date_of_birth), str(self.phone), str(self.account_status), str(self.campID), self.created_time]

    @staticmethod
    def get_volunteer_by_id(volunteerID):  # Get volunteer details by selecting on volunteerID. Returns a list of tuples.
        cursor.execute("SELECT * FROM volunteers WHERE volunteerID = ?", (volunteerID,))
        return [cursor.fetchone()]

    @classmethod  # Insert a volunteer into the database without creating a new instance
    def create_volunteer(cls, volunteer_tuple):
        first_name, last_name, username, password, date_of_birth, phone, campID, created_time = volunteer_tuple
        if Volunteer.check_campID_exist(campID):
            sql = """
                INSERT INTO volunteers (
                first_name, last_name, username, password, date_of_birth, phone, account_status, campID, created_time) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(sql, (first_name, last_name, username,
                                 password, date_of_birth, phone, "Active", campID, created_time))
            conn.commit()
            volunteer_id = cursor.execute("SELECT last_insert_rowid() FROM volunteers").fetchone()[0]
            return Volunteer.get_volunteer_by_id(volunteer_id)
        else:
            return 'Camp campID does not exist'

    @staticmethod  # Update an volunteer by selecting on volunteerID
    def update_volunteer(volunteerID, first_name=None, last_name=None, username=None,
                         password=None, date_of_birth=None, phone=None, account_status=None, campID=None):
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
            query.append("campID = ?")
            params.append(campID)

        params.append(volunteerID)
        q = f"""UPDATE volunteers SET {', '.join(query)} WHERE volunteerID = ?"""
        print(f'q: {q}')
        print(f'params: {params}')
        cursor.execute(q, params)
        conn.commit()
        return Volunteer.get_volunteer_by_id(volunteerID=volunteerID)

    @staticmethod
    def delete_volunteer(volunteerID):  # Delete a volunteer by selecting on volunteerID
        cursor.execute("DELETE FROM volunteers WHERE volunteerID = ?", (volunteerID,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            print(f"Volunteer {volunteerID} has been deleted")
        else:
            print(f"Volunteer {volunteerID} has not been deleted")

    @staticmethod  # Get volunteer details by selecting on any combination of attributes. Can be used to find the
    # volunteerID which can then be used in the delete and update methods. Returns a list of tuples.
    def get_volunteer(volunteerID=None, first_name=None, last_name=None, username=None,
                      password=None, date_of_birth=None, phone=None, account_status=None, campID=None, inclue_admin=False):
        if inclue_admin:
            query = "SELECT * FROM volunteers WHERE volunteerID IS NOT NULL" 
        else:
            query = "SELECT * FROM volunteers WHERE campID IS NOT NULL"
        if volunteerID:
            query += f" AND volunteerID = {volunteerID}"
        if first_name:
            query += f" AND first_name LIKE '%{first_name}'"
        if last_name:
            query += f" AND last_name LIKE '%{last_name}%'"
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

        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod
    def get_all_volunteers():  # Gets all volunteers. Returns a list of tuples.
        cursor.execute("SELECT * FROM volunteers")
        return cursor.fetchall()

    @staticmethod  # Returns all usernames of active volunteers only. Perhaps useful for the login.
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
        query = []
        params = []
        camps = Camp.get_camp(planID=planID)
        campIDs = [camps[i][0] for i in range(len(camps))]
        for campID in campIDs:
            query.append("campID = ?")
            params.append(campID)
        cursor.execute(f"""SELECT * FROM volunteers WHERE {' OR '.join(query)}""", params)
        return cursor.fetchall()