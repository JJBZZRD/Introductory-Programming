from .config import conn, cursor
from .plan import Plan


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
        conn.commit()

        self.campID = cursor.execute("SELECT last_insert_rowid() FROM camps").fetchone()[0]

    @classmethod  # Insert a camp into the database without creating a new instance
    def create_camp(cls, location, max_shelter, water, max_water, food, max_food, medical_supplies,
                    max_medical_supplies, planID):
        camp = Camp(location, max_shelter, water, max_water, food, max_food, medical_supplies,
                    max_medical_supplies, planID)
        if Camp.check_planID_exist(planID) is not None:
            camp.insert_camp()
            campID = cursor.execute("SELECT last_insert_rowid() FROM camps").fetchone()[0]
            return Camp.get_campID(campID=campID)
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
        return Camp.get_campID(campID=campID)

    @staticmethod
    def get_camp(filter, filename, infor):
        """
        Display the camp information based on the campName

        Parameters:
            campName (str): the camp name.
            filename (str): the csv file that stores the camp information, including camp name, volunteer, and resources
            infor (str): the information that want to display.

        Returns:
            float: the information you want to show
            or
            False: if the information is not found in the csv file or file does not exist.
        """
        """
        match filter:
            case "name":
                if value:
                    volunteers = DataAccess.get_camp_by_name(value)
            case "volunteer":
                volunteers = DataAccess.get_camp_by_volunteer(value)
            case "admin":
                volunteers = DataAccess.get_camp_by_admin(value)
            case _:
                return "You need to specify the filter name and value"
        return volunteers
        """
        try:
            file_instance = open(filename, encoding='UTF8')
            csv_reader = csv.reader(file_instance)
            first_row = next(csv_reader, None)

            var = first_row.index(infor) if infor in first_row else None

            if var is not None:
                for line in csv_reader:
                    if campName == line[0]:
                        return line[var]
            else:
                # the case that the information is not found in the CSV file
                print("Information '{", infor, "}' not found in the CSV file.")
                return False
        except FileNotFoundError:
            # the case where the CSV file doesn't exist
            print("Error: '" + filename + "' file not found.")
            return False

    @staticmethod
    def edit_campInfor(campName, filename, infor):
        """
        Edit the camp information based on the campName

        Parameters:
            campName (str): the camp name.
            filename (str): the csv file that stores the camp information, including camp name, volunteer, and resources
            infor (str): the information that you want to edit.

        Returns:
            no returns but give a new csv file after editing.
        """
        new_val = float(input("Enter a positive number: "))
        try:
            if new_val <= 0:
                # case that the value of new attribute is negative
                raise ValueError("Please enter a positive number.")
            file_instance = open(filename, 'r+', encoding='UTF8')
            csv_reader = csv.reader(file_instance)
            first_row = next(csv_reader, None)

            attr = first_row.index(infor) if infor in first_row else None
            if attr is not None:
                origin = [first_row]
                count = 0
                for row in csv_reader:
                    if row[0] == campName:
                        row[attr] = new_val
                        count += 1
                    origin.append(row)
                if count == 0:
                    # the case that the camp is not exist
                    raise IndexError("The camp is not exist.")
            else:
                # the case where the attribute is not found
                raise TypeError("The attribute is not found in this file.")

            file_instance = open(filename, 'w', encoding='UTF8', newline='')
            csv_writer = csv.writer(file_instance)
            csv_writer.writerows(origin)
        except ValueError as ve:
            print("Value error.", ve)
        except IndexError as ie:
            print("You enter an invalid camp name: ", ie)
        except TypeError as te:
            print("You enter an invalid attribute: ", te)
        except FileNotFoundError:
            print("Error: '" + filename + "' file not found.")
