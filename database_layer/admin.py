from config import conn, cursor


class Admin:
    def __init__(self, first_name, last_name, username, date_of_birth, password, phone):
        self.adminID = None,
        self.first_name = first_name,
        self.last_name = last_name,
        self.username = username,
        self.password = password,
        self.date_of_birth = date_of_birth,
        self.phone = phone

    def insert_admin(self):  # Insert an existing instance of a admin into the database
        sql = """
            INSERT INTO admins (
            first_name, last_name, username, password, date_of_birth, phone) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.first_name, self.last_name, self.username,
                             self.password, self.date_of_birth, self.phone))
        conn.commit()

        self.adminID = cursor.execute("SELECT last_insert_rowid() FROM admins").fetchone()[0]

    @classmethod  # Insert a admin into the database without creating a new instance
    def create_admin(cls, first_name, last_name, username, password, date_of_birth, phone):
        admin = Admin(first_name, last_name, username, password, date_of_birth, phone)
        admin.insert_admin()

    @staticmethod  # Update an admin by selecting on adminID
    def update_admin(adminID, first_name=None, last_name=None, username=None,
                     password=None, date_of_birth=None, phone=None):
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

        params.append(adminID)
        cursor.execute(f"""UPDATE admins SET {', '.join(query)} WHERE adminID = ?""", params)
        conn.commit()

    @staticmethod
    def delete_admin(adminID):  # Delete a admin by selecting on adminID
        cursor.execute("DELETE FROM admins WHERE adminID = ?", (adminID,))
        conn.commit()

    @staticmethod
    def get_adminID(adminID):  # Get admin details by selecting on adminID. Returns a list of tuples.
        cursor.execute("SELECT * FROM admins WHERE adminID = ?", (adminID,))
        return cursor.fetchone()

    @staticmethod  # Get admin details by selecting on any combination of attributes. Can be used to find the
    # adminID which can then be used in the delete and update methods. Returns a list of tuples.
    def get_admin(adminID=None, first_name=None, last_name=None, username=None,
                  password=None, date_of_birth=None, phone=None):
        query = []
        params = []

        if adminID is not None:
            query.append("adminID = ?")
            params.append(adminID)
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

        cursor.execute(f"""SELECT * FROM admins WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod  # Similar to the get_refugee function but using sqlite like to create a sort of search function.
    def search_admin(adminID=None, first_name=None, last_name=None, username=None,
                  password=None, date_of_birth=None, phone=None):
        query = []
        params = []

        if adminID is not None:
            query.append("adminID LIKE ?")
            params.append(f"{adminID}%")
        if first_name is not None:
            query.append("first_name LIKE ?")
            params.append(f"{first_name}%")
        if last_name is not None:
            query.append("last_name LIKE ?")
            params.append(f"{last_name}%")
        if username is not None:
            query.append("username LIKE ?")
            params.append(f"{username}%")
        if password is not None:
            query.append("password LIKE ?")
            params.append(f"{password}%")
        if date_of_birth is not None:
            query.append("date_of_birth LIKE ?")
            params.append(f"{date_of_birth}%")
        if phone is not None:
            query.append("phone LIKE ?")
            params.append(f"{phone}%")

        cursor.execute(f"""SELECT * FROM admins WHERE {' AND '.join(query)}""", params)
        return cursor.fetchall()

    @staticmethod
    def get_all_admins():  # Gets all admins. Returns a list of tuples.
        cursor.execute("SELECT * FROM admins")
        return cursor.fetchall()
