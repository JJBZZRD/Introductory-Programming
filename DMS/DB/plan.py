from .config import conn, cursor


class Plan:  # Plan class has attributes matching columns in table
    def __init__(self, planID, start_date, end_date, name, country, event_name, description, water, food, medical_supplies, shelter):
        self.planID = planID
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.country = country
        self.event_name = event_name
        self.description = description
        self.water = water
        self.food = food
        self.medical_supplies = medical_supplies
        self.shelter = shelter
        self.end_date_datetime = None
        self.status = None
    @classmethod
    def init_from_tuple(cls, plan_tuple):
        return cls(*plan_tuple)

    def display_info(self):
        return [str(self.planID), str(self.name), str(self.country), str(self.event_name), str(self.description),
                str(self.start_date), str(self.end_date)]

    @staticmethod
    def get_plan_by_id(planID):  # Get plan details by selecting on planID. Returns a list of tuples.
        cursor.execute("SELECT * FROM plans WHERE planID = ?", (planID,))
        return [cursor.fetchone()]

    @classmethod  # Insert a plan into the database
    def create_plan(cls, plan_tuple):
        start_date, end_date, name, country, event_name, description, water, food, medical_supplies, shelter = plan_tuple
        sql = """
            INSERT INTO plans (
                start_date, end_date, name, country, event_name, description, water, food, medical_supplies, shelter) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        cursor.execute(sql, (start_date, end_date, name, country, event_name, description, water, food, medical_supplies, shelter))
        conn.commit()
        plan_id = cursor.execute("SELECT last_insert_rowid() FROM plans").fetchone()[0]
        return Plan.get_plan_by_id(plan_id)


    @staticmethod  # Update a plan by selecting on planID
    def update_plan(planID, start_date=None, end_date=None, name=None, country=None, event_name=None, description=None, water=None, food=None, shelter=None, medical_supplies=None):

        query = []
        params = []

        if start_date is not None:
            query.append("start_date = ?")
            params.append(start_date)
        if end_date is not None:
            query.append("end_date = ?")
            params.append(end_date)
        if name is not None:
            query.append("name = ?")
            params.append(name)
        if country is not None:
            query.append("country = ?")
            params.append(country)
        if event_name is not None:
            query.append("event_name = ?")
            params.append(event_name)
        if description is not None:
            query.append("description = ?")
            params.append(description)
        if water is not None:
            query.append("water = ?")
            params.append(water)
        if food is not None:
            query.append("food = ?")
            params.append(food)
        if shelter is not None:
            query.append("shelter = ?")
            params.append(shelter)
        if medical_supplies is not None:
            query.append("medical_supplies = ?")
            params.append(medical_supplies)
        
        params.append(planID)
        cursor.execute(f"""UPDATE plans SET {', '.join(query)} WHERE planID = ?""", params)
        conn.commit()
        return Plan.get_plan(planID=planID)

    @staticmethod
    def delete_plan(planID):  # Delete a plan by selecting on planID
        cursor.execute("DELETE FROM plans WHERE planID = ?", (planID,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            print(f"Plan {planID} has been deleted")
            return True
        else:
            print(f"Plan {planID} has not been deleted")
            return False

    @staticmethod
    def get_plan(planID=None, start_date=None, end_date=None, name=None, country=None, event_name=None, description=None):

        query = "SELECT * FROM plans WHERE planID IS NOT NULL"

        if planID:
            query += f" AND planID = {planID}"
        if start_date:
            query += f" AND start_date = '{start_date}'"
        if end_date:
            query += f" AND end_date = '{end_date}'"
        if name:
            query += f" AND name LIKE '%{name}%'"
        if country:
            query += f" AND country = '{country}'"
        if event_name:
            query += f" AND event_name LIKE '%{event_name}%'"
        if description:
            query += f" AND description LIKE '%{description}%'"

        # print(query)
        cursor.execute(query)
        return cursor.fetchall()


    @staticmethod
    def get_all_plans():  # Gets all plans. Returns a list of tuples.
        cursor.execute("SELECT * FROM plans")
        return cursor.fetchall()

    @staticmethod
    def get_total_resources(planID):
        q = f"""
            SELECT SUM(shelter) as sum_shelter,
                SUM(food) as sum_food,
                SUM(water) as sum_water,
                SUM(medical_supplies) as sum_med
            FROM camps
            WHERE planID = {planID}
            GROUP BY planID
            """
        cursor.execute(q)
        return cursor.fetchall()

    @staticmethod
    def get_plan_families(planID):
        q = f"""
        SELECT familyID
        FROM refugees
        LEFT JOIN camps ON refugees.campID = camps.campID
        WHERE camps.planID = {planID}
        GROUP BY familyID
        """
        cursor.execute(q)
        return cursor.fetchall()
