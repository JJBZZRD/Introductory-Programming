from .config import conn, cursor


class Plan:  # Plan class has attributes matching columns in table
    def __init__(self, planID, start_date, end_date, name, region, event_name, description):
        self.planID = planID
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.region = region
        self.event_name = event_name
        self.description = description

    @classmethod
    def init_from_tuple(cls, plan_tuple):
        return cls(*plan_tuple)

    def display_info(self):
        return [str(self.planID), str(self.start_date), str(self.end_date), str(self.name), str(self.region), str(self.event_name), str(self.description)]

    @staticmethod
    def get_plan_by_id(planID):  # Get plan details by selecting on planID. Returns a list of tuples.
        cursor.execute("SELECT * FROM plans WHERE planID = ?", (planID,))
        return [cursor.fetchone()]

    @classmethod  # Insert a plan into the database
    def create_plan(cls, plan_tuple):
        start_date, end_date, name, region, event_name, description = plan_tuple
        sql = """
            INSERT INTO plans (
                start_date, end_date, name, region, event_name, description) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
        cursor.execute(sql, (start_date, end_date, name, region, event_name, description))
        conn.commit()
        plan_id = cursor.execute("SELECT last_insert_rowid() FROM plans").fetchone()[0]
        return Plan.get_plan_by_id(plan_id)


    @staticmethod  # Update a plan by selecting on planID
    def update_plan(planID, start_date=None, end_date=None, name=None, region=None, event_name=None, description=None):

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
        if region is not None:
            query.append("region = ?")
            params.append(region)
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
    def get_plan(planID=None, start_date=None, end_date=None, name=None, region=None, event_name=None, description=None):

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
        if region is not None:
            query.append("region LIKE ?")
            params.append(f"{region}%")
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