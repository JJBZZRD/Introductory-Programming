from config import conn, cursor


class Camp:  # Camp class has attributes matching columns in table
    def __init__(self, location, max_shelter, water, max_water, food, max_food, medical_supplies,
                 max_medical_supplies, planID):
        self.campID = None
        self.location = location
        self.max_shelter = max_shelter
        self.water = water
        self.max_water = max_water
        self.food = food
        self.max_food = max_food
        self.medical_supplies = medical_supplies
        self.max_medical_supplies = max_medical_supplies
        self.planID = planID

    def insert_camp(self):  # Insert an existing instance of a camp into the database
        sql = """
            INSERT INTO camps (
                location, max_shelter, water, max_water, food, max_food, medical_supplies,
                max_medical_supplies, planID) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.location, self.max_shelter, self.water, self.max_water, self.food,
                             self.max_food, self.medical_supplies, self.max_medical_supplies, self.planID))
        self.campID = cursor.execute("SELECT last_insert_rowid() FROM camps").fetchone()[0]

    @classmethod  # Insert a camp into the database without creating a new instance
    def create_camp(cls, location, max_shelter, water, max_water, food, max_food, medical_supplies,
                    max_medical_supplies, planID):
        camp = Camp(location, max_shelter, water, max_water, food, max_food, medical_supplies,
                    max_medical_supplies, planID)
        camp.insert_camp()

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

    @staticmethod
    def delete_camp(campID):  # Delete a camp by selecting on campID
        cursor.execute("DELETE FROM camps WHERE campID = ?", (campID,))
        conn.commit()

    @staticmethod
    def get_campID(campID):  # Get camp details by selecting on campID. Returns a list of tuples.
        cursor.execute("SELECT * FROM camps WHERE campID = ?", (campID,))
        return cursor.fetchone()

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

        cursor.execute(f"""SELECT * FROM camps WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod  # Similar to the get_camp function but using sqlite like to create a sort of search function.
    def search_camp(campID=None, location=None, max_shelter=None, water=None, max_water=None, food=None, max_food=None,
                     medical_supplies=None, max_medical_supplies=None, planID=None):

        query = []
        params = []

        if campID is not None:
            query.append("campID LIKE ?")
            params.append(f"{campID}%")
        if location is not None:
            query.append("location LIKE ?")
            params.append(f"{location}%")
        if max_shelter is not None:
            query.append("max_shelter LIKE ?")
            params.append(f"{max_shelter}%")
        if water is not None:
            query.append("water LIKE ?")
            params.append(f"{water}%")
        if max_water is not None:
            query.append("max_water LIKE ?")
            params.append(f"{max_water}%")
        if food is not None:
            query.append("food LIKE ?")
            params.append(f"{food}%")
        if max_food is not None:
            query.append("max_food LIKE ?")
            params.append(f"{max_food}%")
        if medical_supplies is not None:
            query.append("medical_supplies LIKE ?")
            params.append(f"{medical_supplies}%")
        if max_medical_supplies is not None:
            query.append("max_medical_supplies LIKE ?")
            params.append(f"{max_medical_supplies}%")
        if planID is not None:
            query.append("planID LIKE ?")
            params.append(f"{planID}%")

        cursor.execute(f"SELECT * FROM camps WHERE {' AND '.join(query)}", params)

        return cursor.fetchall()

    @staticmethod
    def get_all_camps():  # Gets all camps. Returns a list of tuples.
        cursor.execute("SELECT * FROM camps")
        return cursor.fetchall()
