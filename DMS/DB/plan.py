from .config import conn, cursor


class Plan:  # Plan class has attributes matching columns in table
    def __init__(self, planID, start_date, end_date, name, country, event_name, description):
        self.planID = planID
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.country = country
        self.event_name = event_name
        self.description = description
        self.water = None
        self.food = None
        self.shelter = None
        self.medical_supplies = None

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
        start_date, end_date, name, country, event_name, description = plan_tuple
        sql = """
            INSERT INTO plans (
                start_date, end_date, name, country, event_name, description) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
        cursor.execute(sql, (start_date, end_date, name, country, event_name, description))
        conn.commit()
        plan_id = cursor.execute("SELECT last_insert_rowid() FROM plans").fetchone()[0]
        return Plan.get_plan_by_id(plan_id)


    @staticmethod  # Update a plan by selecting on planID
    def update_plan(planID, start_date=None, end_date=None, name=None, country=None, event_name=None, description=None):

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
        else:
            print(f"Plan {planID} has not been deleted")

    @staticmethod  # Get plan details by selecting on any combination of attributes. Can be used to find the
    # planID which can then be used in the delete and update methods. Returns a list of tuples.
    def get_plan(planID=None, start_date=None, end_date=None, name=None, country=None, event_name=None, description=None):

        query = []
        params = []

        if planID is not None:
            query.append("planID = ?")
            params.append(planID)
        if start_date is not None:
            query.append("start_date = ?")
            params.append(start_date)
        if end_date is not None:
            query.append("end_date = ?")
            params.append(end_date)
        if name is not None:
            query.append("name LIKE ?")
            params.append(f"{name}%")
        if country is not None:
            query.append("country LIKE ?")
            params.append(f"{country}%")
        if event_name is not None:
            query.append("event_name LIKE ?")
            params.append(f"{event_name}%")
        if description is not None:
            query.append("description LIKE ?")
            params.append(f"{description}%")

        cursor.execute(f"""SELECT * FROM plans WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod
    def get_all_plans():  # Gets all plans. Returns a list of tuples.
        cursor.execute("SELECT * FROM plans")
        return cursor.fetchall()

    @staticmethod
    def get_total_resources(planID):
        from .camp import Camp as pc
        shelter = []
        food = []
        water = []
        medical_supplies = []
        total_shelter = 0
        total_food = 0
        total_water = 0
        total_medical_supplies = 0
        camps_tuples = pc.get_camp(planID=planID)
        campIDs = [camps_tuples[i][0] for i in range(len(camps_tuples))]
        for campID in campIDs:
            camps = pc.get_camp_by_id(campID)
            s = camps[0][2]
            shelter.append(s)
            f = camps[0][5]
            food.append(f)
            w = camps[0][3]
            water.append(w)
            m = camps[0][7]
            medical_supplies.append(m)
        for i in shelter:
            total_shelter += i
        for i in food:
            total_food += i
        for i in water:
            total_water += i
        for i in medical_supplies:
            total_medical_supplies += i
        return [total_food, total_water, total_shelter, total_medical_supplies]
