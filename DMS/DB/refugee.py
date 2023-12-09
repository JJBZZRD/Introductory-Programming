from .config import conn, cursor
from .camp import Camp


class Refugee:  # Refugee class has attributes matching columns in table
    def __init__(self, refugeeID, first_name, last_name, date_of_birth, gender, familyID, campID,
                 triage_category, medical_conditions, vital_status):
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

    @classmethod
    def init_from_tuple(cls, refugee_tuple):
        return cls(*refugee_tuple)

    def display_info(self):
        return [str(self.refugeeID), str(self.first_name), str(self.last_name),
                str(self.date_of_birth), str(self.gender), str(self.familyID),
                str(self.campID), str(self.triage_category), str(self.medical_conditions),
                str(self.vital_status)]

    @staticmethod
    def get_refugee_by_id(refugeeID):  # Get refugee details by selecting on refugeeID. Returns a list of tuples.
        cursor.execute("SELECT * FROM refugees WHERE refugeeID = ?", (refugeeID,))
        return [cursor.fetchone()]

    @classmethod    # Insert a refugee into the database without creating a new instance
    def create_refugee(cls, refugee_tuple):
        (first_name, last_name, date_of_birth, gender, familyID, campID, triage_category,
         medical_conditions, vital_status) = refugee_tuple
        if Refugee.check_campID_exist(campID):
            sql = """
                INSERT INTO refugees (
                first_name, last_name, date_of_birth, gender, familyID, campID, triage_category, medical_conditions, vital_status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(sql, (first_name, last_name, date_of_birth, gender,
                                 familyID, campID, triage_category, medical_conditions, vital_status))
            conn.commit()
            refugee_id = cursor.execute("SELECT last_insert_rowid() FROM refugees").fetchone()[0]
            return Refugee.get_refugee_by_id(refugee_id)
        else:
            return 'Camp campID does not exist'

    @staticmethod  # Update a refugee by selecting on refugeeID
    def update_refugee(refugeeID, first_name=None, last_name=None, date_of_birth=None, gender=None,
                       familyID=None, campID=None, triage_category=None, medical_conditions=None, vital_status=None):
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
        cursor.execute(f"""UPDATE refugees SET {', '.join(query)} WHERE refugeeID = ?""", params)
        conn.commit()
        return Refugee.get_refugee_by_id(refugeeID)

    @staticmethod
    def delete_refugee(refugeeID):  # Delete a refugee by selecting on refugeeID
        cursor.execute("DELETE FROM refugees WHERE refugeeID = ?", (refugeeID,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            print(f"Refugee {refugeeID} has been deleted")
        else:
            print(f"Refugee {refugeeID} has not been deleted")

    @staticmethod  # Get refugee details by selecting on any combination of attributes. Can be used to find the
    # refugeeID which can then be used in the delete and update methods. Returns a list of tuples.
    def get_refugee(refugeeID=None, first_name=None, last_name=None, date_of_birth=None, gender=None,
                    familyID=None, campID=None, triage_category=None, medical_conditions=None,
                    vital_status=None):
        query = "SELECT * FROM refugees WHERE refugeeID IS NOT NULL"

        if refugeeID:
            query += f" AND refugeeID = {refugeeID}"
        if first_name:
            query += f" AND first_name LIKE '%{first_name}%'"
        if last_name:
            query += f" AND last_name LIKE '%{last_name}%'" 
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

        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_all_refugees():  # Gets all refugees. Returns a list of tuples.
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
        query = []
        params = []
        camps = Camp.get_camp(planID=planID)
        campIDs = [camps[i][0] for i in range(len(camps))]
        for campID in campIDs:
            query.append("campID = ?")
            params.append(campID)
        cursor.execute(f"""SELECT * FROM refugees WHERE {' OR '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod
    def get_refugees_by_plan(plan_id):
        q = f"""
            SELECT *
            FROM refugees
            WHERE campID IN
                (SELECT campID
                FROM camps
                WHERE planID = {plan_id})
            """
        cursor.execute(q)
        return cursor.fetchall()