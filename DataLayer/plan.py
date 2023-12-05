from config import conn, cursor


class Plan:  # Plan class has attributes matching columns in table
    def __init__(self, *args):
        # Check if the first argument is a tuple and has the correct number of elements
        if len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) in {6, 7}:
            # Unpack the tuple
            unpacked_args = args[0]
        elif len(args) in {6, 7}:
            # Args are individual parameters
            unpacked_args = args
        else:
            raise ValueError("Invalid arguments to Plan constructor")

        # Assign values with default None for planID
        self.planID = unpacked_args[0] if len(unpacked_args) == 7 else None
        self.start_date, self.end_date, self.name, self.region, self.event_name, self.description = unpacked_args[-6:]

    def print_self(self):
        print(self.planID)
        print(self.start_date)
        print(self.end_date)
        print(self.name)
        print(self.region)
        print(self.event_name)
        print(self.description)

    def insert_plan(self):  # Insert an existing instance of a plan into the database
        sql = """
            INSERT INTO plans (
                start_date, end_date, name, region, event_name, description) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
        cursor.execute(sql, (self.start_date, self.end_date, self.region, self.name, self.event_name,
                             self.description))
        conn.commit()

        self.planID = cursor.execute("SELECT last_insert_rowid() FROM plans").fetchone()[0]

    @classmethod  # Insert a plan into the database without creating a new instance
    def create_plan(cls, start_date, end_date, name, region, event_name, description):
        plan = Plan(start_date, end_date, name, region, event_name, description)
        plan.insert_plan()
        planID = cursor.execute("SELECT last_insert_rowid() FROM plans").fetchone()[0]
        return Plan.get_planID(planID=planID)

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

    @staticmethod
    def get_planID(planID):  # Get plan details by selecting on planID. Returns a list of tuples.
        cursor.execute("SELECT * FROM plans WHERE planID = ?", (planID,))
        return cursor.fetchone()

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

        cursor.execute(f"""SELECT * FROM plans WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod  # Similar to the get_plan function but using sqlite like to create a sort of search function.
    def search_plan(planID=None, start_date=None, end_date=None, name=None, region=None, event_name=None,
                 description=None):

        query = []
        params = []

        if planID is not None:
            query.append("planID like ?")
            params.append(f"{planID}%")
        if start_date is not None:
            query.append("start_date like ?")
            params.append(f"{start_date}%")
        if end_date is not None:
            query.append("end_date like ?")
            params.append(f"{end_date}%")
        if name is not None:
            query.append("name like ?")
            params.append(f"{name}%")
        if region is not None:
            query.append("region like ?")
            params.append(f"{region}%")
        if event_name is not None:
            query.append("event_name like ?")
            params.append(f"{event_name}%")
        if description is not None:
            query.append("description like ?")
            params.append(f"{description}%")

        cursor.execute(f"""SELECT * FROM plans WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod
    def get_all_plans():  # Gets all plans. Returns a list of tuples.
        cursor.execute("SELECT * FROM plans")
        return cursor.fetchall()
