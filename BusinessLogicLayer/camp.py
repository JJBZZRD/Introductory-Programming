import csv
from DataAccessLayer.data_access import DataAccess

class CampDataRetrieve:
    """
    A class representing a camp
    """
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
