from config import conn, cursor
from camp import Camp


class Refugee:  # Refugee class has attributes matching columns in table
    def __init__(self, first_name, last_name, date_of_birth, familyID, campID, medical_condition):
        self.refugeeID = None
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.familyID = familyID
        self.campID = campID
        self.medical_condition = medical_condition

    def insert_refugee(self):  # Insert an existing instance of a refugee into the database
        sql = """
            INSERT INTO refugees (
            first_name, last_name, date_of_birth, familyID, campID, medical_condition) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
        cursor.execute(sql, (self.first_name, self.last_name, self.date_of_birth,
                             self.familyID, self.campID, self.medical_condition))
        conn.commit()

        self.refugeeID = cursor.execute("SELECT last_insert_rowid() FROM refugees").fetchone()[0]

    @classmethod    # Insert a refugee into the database without creating a new instance
    def create_refugee(cls, first_name, last_name, date_of_birth, familyID, campID, medical_condition):
        refugee = Refugee(first_name, last_name, date_of_birth, familyID, campID, medical_condition)
        if Refugee.check_campID_exist(campID) is not None:
            refugee.insert_refugee()
            refugeeID = cursor.execute("SELECT last_insert_rowid() FROM refugees").fetchone()[0]
            return refugee.get_refugeeID(refugeeID=refugeeID)
        else:
            return 'Camp campID does not exist'

    @staticmethod  # Update a refugee by selecting on refugeeID
    def update_refugee(refugeeID, first_name=None, last_name=None, date_of_birth=None,
                       familyID=None, campID=None, medical_condition=None):
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
        if familyID is not None:
            query.append("familyID = ?")
            params.append(familyID)
        if campID is not None:
            query.append("campID = ?")
            params.append(campID)
        if medical_condition is not None:
            query.append("medical_condition = ?")
            params.append(medical_condition)

        params.append(refugeeID)
        cursor.execute(f"""UPDATE refugees SET {', '.join(query)} WHERE refugeeID = ?""", params)
        conn.commit()
        return Refugee.get_refugeeID(refugeeID=refugeeID)

    @staticmethod
    def delete_refugee(refugeeID):  # Delete a refugee by selecting on refugeeID
        cursor.execute("DELETE FROM refugees WHERE refugeeID = ?", (refugeeID,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            print(f"Refugee {refugeeID} has been deleted")
        else:
            print(f"Refugee {refugeeID} has not been deleted")

    @staticmethod
    def get_refugeeID(refugeeID):  # Get refugee details by selecting on refugeeID. Returns a list of tuples.
        cursor.execute("SELECT * FROM refugees WHERE refugeeID = ?", (refugeeID,))
        return cursor.fetchone()

    @staticmethod  # Get refugee details by selecting on any combination of attributes. Can be used to find the
    # refugeeID which can then be used in the delete and update methods. Returns a list of tuples.
    def get_refugee(refugeeID=None, first_name=None, last_name=None, date_of_birth=None,
                    familyID=None, campID=None, medical_condition=None):
        query = []
        params = []

        if refugeeID is not None:
            query.append("refugeeID = ?")
            params.append(refugeeID)
        if first_name is not None:
            query.append("first_name = ?")
            params.append(first_name)
        if last_name is not None:
            query.append("last_name = ?")
            params.append(last_name)
        if date_of_birth is not None:
            query.append("date_of_birth = ?")
            params.append(date_of_birth)
        if familyID is not None:
            query.append("familyID = ?")
            params.append(familyID)
        if campID is not None:
            query.append("campID = ?")
            params.append(campID)
        if medical_condition is not None:
            query.append("medical_condition = ?")
            params.append(medical_condition)

        cursor.execute(f"""SELECT * FROM refugees WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod  # Similar to the get_refugee function but using sqlite like to create a sort of search function.
    def search_refugee(refugeeID=None, first_name=None, last_name=None, date_of_birth=None,
                    familyID=None, campID=None, medical_condition=None):
        query = []
        params = []

        if refugeeID is not None:
            query.append("refugeeID LIKE ?")
            params.append(f"{refugeeID}%")
        if first_name is not None:
            query.append("first_name LIKE ?")
            params.append(f"{first_name}%")
        if last_name is not None:
            query.append("last_name LIKE ?")
            params.append(f"{last_name}%")
        if date_of_birth is not None:
            query.append("date_of_birth LIKE ?")
            params.append(f"{date_of_birth}%")
        if familyID is not None:
            query.append("familyID LIKE ?")
            params.append(f"{familyID}%")
        if campID is not None:
            query.append("campID LIKE ?")
            params.append(f"{campID}%")
        if medical_condition is not None:
            query.append("medical_condition LIKE ?")
            params.append(f"{medical_condition}%")

        cursor.execute(f"""SELECT * FROM refugees WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod
    def get_all_refugees():  # Gets all refugees. Returns a list of tuples.
        cursor.execute("SELECT * FROM refugees")
        return cursor.fetchall()

    @staticmethod
    def check_campID_exist(campID):
        camp = Camp.get_campID(campID)
        if camp is not None:
            return True
        else:
            return False