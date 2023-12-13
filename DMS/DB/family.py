from .config import conn, cursor


class Family:  # Family class has attributes matching columns in table
    def __init__(self, familyID, family_name, lead_family_memberID):
        self.familyID = familyID
        self.family_name = family_name
        self.lead_family_memberID = lead_family_memberID

    @classmethod
    def init_from_tuple(cls, family_tuple):
        return cls(*family_tuple)

    def display_info(self):
        return [str(self.familyID), str(self.family_name), str(self.lead_family_memberID)]

    @staticmethod
    def get_family_by_id(familyID):  # Get refugee details by selecting on refugeeID. Returns a list of tuples.
        cursor.execute("SELECT * FROM refugees WHERE refugeeID = ?", (familyID,))
        return [cursor.fetchone()]

    # @classmethod    # Insert a refugee into the database without creating a new instance
    # def create_refugee(cls, refugee_tuple):
    #     first_name, last_name, date_of_birth, gender, familyID, campID, medical_condition, vital_status = refugee_tuple
    #     if Refugee.check_campID_exist(campID):
    #         sql = """
    #             INSERT INTO refugees (
    #             first_name, last_name, date_of_birth, gender, familyID, campID, medical_condition, vital_status)
    #             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    #             """
    #         cursor.execute(sql, (first_name, last_name, date_of_birth, gender,
    #                              familyID, campID, medical_condition, vital_status))
    #         conn.commit()
    #         refugee_id = cursor.execute("SELECT last_insert_rowid() FROM refugees").fetchone()[0]
    #         return Refugee.get_refugee_by_id(refugee_id)
    #     else:
    #         return 'Camp campID does not exist'

    # @staticmethod  # Update a refugee by selecting on refugeeID
    # def update_refugee(refugeeID, first_name=None, last_name=None, date_of_birth=None, gender=None,
    #                    familyID=None, campID=None, medical_condition=None, vital_status=None):
    #     query = []
    #     params = []
    #
    #     if first_name is not None:
    #         query.append("first_name = ?")
    #         params.append(first_name)
    #     if last_name is not None:
    #         query.append("last_name = ?")
    #         params.append(last_name)
    #     if date_of_birth is not None:
    #         query.append("date_of_birth = ?")
    #         params.append(date_of_birth)
    #     if gender is not None:
    #         query.append("gender = ?")
    #         params.append(gender)
    #     if familyID is not None:
    #         query.append("familyID = ?")
    #         params.append(familyID)
    #     if campID is not None:
    #         query.append("campID = ?")
    #         params.append(campID)
    #     if medical_conditions is not None:
    #         query.append("medical_conditions = ?")
    #         params.append(medical_condition)
    #     if vital_status is not None:
    #         query.append("vital_status = ?")
    #         params.append(vital_status)
    #
    #     params.append(refugeeID)
    #     cursor.execute(f"""UPDATE refugees SET {', '.join(query)} WHERE refugeeID = ?""", params)
    #     conn.commit()
    #     return Refugee.get_refugee_by_id(refugeeID)

    # @staticmethod
    # def delete_refugee(refugeeID):  # Delete a refugee by selecting on refugeeID
    #     cursor.execute("DELETE FROM refugees WHERE refugeeID = ?", (refugeeID,))
    #     rows_deleted = cursor.rowcount
    #     conn.commit()
    #     if rows_deleted > 0:
    #         print(f"Refugee {refugeeID} has been deleted")
    #     else:
    #         print(f"Refugee {refugeeID} has not been deleted")

    #
    # @staticmethod  # Get refugee details by selecting on any combination of attributes. Can be used to find the
    # # refugeeID which can then be used in the delete and update methods. Returns a list of tuples.
    # def get_refugee(refugeeID=None, first_name=None, last_name=None, date_of_birth=None, gender=None,
    #                 familyID=None, campID=None, medical_condition=None, vital_status=None):
    #     query = []
    #     params = []
    #
    #     if refugeeID is not None:
    #         query.append("refugeeID = ?")
    #         params.append(refugeeID)
    #     if first_name is not None:
    #         query.append("first_name LIKE ?")
    #         params.append(f"{first_name}%")
    #     if last_name is not None:
    #         query.append("last_name LIKE ?")
    #         params.append(f"{last_name}%")
    #     if date_of_birth is not None:
    #         query.append("date_of_birth = ?")
    #         params.append(date_of_birth)
    #     if gender is not None:
    #         query.append("gender = ?")
    #         params.append(gender)
    #     if familyID is not None:
    #         query.append("familyID = ?")
    #         params.append(familyID)
    #     if campID is not None:
    #         query.append("campID = ?")
    #         params.append(campID)
    #     if medical_conditions is not None:
    #         query.append("medical_conditions LIKE ?")
    #         params.append(f"{medical_condition}%")
    #     if vital_status is not None:
    #         query.append("vital_status = ?")
    #         params.append(vital_status)
    #
    #     cursor.execute(f"""SELECT * FROM refugees WHERE {' AND '.join(query)}""", params)
    #     return cursor.fetchall()
    #
    # @staticmethod
    # def get_all_refugees():  # Gets all refugees. Returns a list of tuples.
    #     cursor.execute("SELECT * FROM refugees")
    #     return cursor.fetchall()
    #
    # @staticmethod
    # def check_campID_exist(campID):
    #     camp = Camp.get_campID(campID)
    #     if camp is not None:
    #         return True
    #     else:
    #         return False

    # @staticmethod
    # def get_by_planID(planID):
    #     query = []
    #     params = []
    #     camps = Camp.get_camp(planID=planID)
    #     campIDs = [camps[i][0] for i in range(len(camps))]
    #     for campID in campIDs:
    #         query.append("campID = ?")
    #         params.append(campID)
    #     cursor.execute(f"""SELECT * FROM refugees WHERE {' OR '.join(query)}""", params)
    #     return cursor.fetchall()


