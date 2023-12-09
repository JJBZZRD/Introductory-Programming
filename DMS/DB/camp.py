from .config import conn, cursor
from .plan import Plan


class Camp:  # Camp class has attributes matching columns in table
    def __init__(self, campID, location, max_shelter, water, max_water, food, max_food, medical_supplies,
                 max_medical_supplies, planID):
        self.campID = campID
        self.location = location
        self.max_shelter = max_shelter
        self.water = water
        self.max_water = max_water
        self.food = food
        self.max_food = max_food
        self.medical_supplies = medical_supplies
        self.max_medical_supplies = max_medical_supplies
        self.planID = planID

    @classmethod
    def init_from_tuple(cls, camp_tuple):
        return cls(*camp_tuple)

    def display_info(self):
        return [str(self.campID), str(self.location), str(self.max_shelter), str(self.water), str(self.max_water), str(self.food), str(self.max_food),
                str(self.medical_supplies), str(self.max_medical_supplies), str(self.planID)]

    @staticmethod
    def get_camp_by_id(campID):  # Get camp details by selecting on campID. Returns a list of tuples.
        cursor.execute("SELECT * FROM camps WHERE campID = ?", (campID,))
        return [cursor.fetchone()]

    @classmethod  # Insert a camp into the database without creating a new instance
    def create_camp(cls, camp_tuple):
        location, max_shelter, water, max_water, food, max_food, medical_supplies, max_medical_supplies, planID = camp_tuple
        if Camp.check_planID_exist(planID):
            sql = """
                INSERT INTO camps (
                    location, max_shelter, water, max_water, food, max_food, medical_supplies,
                    max_medical_supplies, planID) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(sql, (location, max_shelter, water, max_water, food,
                                 max_food, medical_supplies, max_medical_supplies, planID))
            conn.commit()
            camp_id = cursor.execute("SELECT last_insert_rowid() FROM camps").fetchone()[0]
            return Camp.get_camp_by_id(camp_id)
        else:
            return 'Plan planID does not exist'
        
    @staticmethod  # Update a camp by selecting on campID
    def update_camp(campID, location=None, max_shelter=None, water=None, max_water=None, food=None, max_food=None,
                    medical_supplies=None, max_medical_supplies=None, planID=None):

        query = []
        params = []

        if location is not None:
            query.append("location = ?")
            params.append(location)
        if max_shelter is not None:
            query.append("max_shelter = ?")
            params.append(max_shelter)
        if water is not None:
            query.append("water = ?")
            params.append(water)
        if max_water is not None:
            query.append("max_water = ?")
            params.append(max_water)
        if food is not None:
            query.append("food = ?")
            params.append(food)
        if max_food is not None:
            query.append("max_food = ?")
            params.append(max_food)
        if medical_supplies is not None:
            query.append("medical_supplies = ?")
            params.append(medical_supplies)
        if max_medical_supplies is not None:
            query.append("max_medical_supplies = ?")
            params.append(max_medical_supplies)
        if planID is not None:
            query.append("planID = ?")
            params.append(planID)

        params.append(campID)
        cursor.execute(f"""UPDATE camps SET {', '.join(query)} WHERE campID = ?""", params)
        conn.commit()
        return Camp.get_camp_by_id(campID)

    @staticmethod
    def delete_camp(campID):  # Delete a camp by selecting on campID
        cursor.execute("DELETE FROM camps WHERE campID = ?", (campID,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            print(f"Camp {campID} has been deleted")
        else:
            print(f"Admin {campID} has not been deleted")


    @staticmethod  # Get camp details by selecting on any combination of attributes. Can be used to find the
    # campID which can then be used in the delete and update methods. Returns a list of tuples.
    def get_camp(campID=None, location=None, max_shelter=None, water=None, max_water=None, food=None, max_food=None,
                 medical_supplies=None, max_medical_supplies=None, planID=None):

        query = []
        params = []

        if campID is not None:
            query.append("campID = ?")
            params.append(campID)
        if location is not None:
            query.append("location LIKE ?")
            params.append(f"{location}%")
        if max_shelter is not None:
            query.append("max_shelter = ?")
            params.append(max_shelter)
        if water is not None:
            query.append("water = ?")
            params.append(water)
        if max_water is not None:
            query.append("max_water = ?")
            params.append(max_water)
        if food is not None:
            query.append("food = ?")
            params.append(food)
        if max_food is not None:
            query.append("max_food = ?")
            params.append(max_food)
        if medical_supplies is not None:
            query.append("medical_supplies = ?")
            params.append(medical_supplies)
        if max_medical_supplies is not None:
            query.append("max_medical_supplies = ?")
            params.append(max_medical_supplies)
        if planID is not None:
            query.append("planID = ?")
            params.append(planID)

        cursor.execute(f"""SELECT * FROM camps WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()
    
    @staticmethod
    def get_all_camps():  # Gets all camps. Returns a list of tuples.
        cursor.execute("SELECT * FROM camps")
        return cursor.fetchall()

    @staticmethod
    def check_planID_exist(planID):
        plan = Plan.get_plan_by_id(planID)
        if plan is not None:
            return True
        else:
            return False
    
    @staticmethod
    def get_stats_triage_category(campID):
        q = f"""SELECT vital_status, triage_category, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM refugees) AS percentage
                FROM refugees
                WHERE campID = {campID}
                GROUP BY triage_category, vital_status"""
        print(q)
        cursor.execute(q)
        return cursor.fetchall()