import csv

class UserDataAccess:
    """
    UserDataAccess provides functionality to interact with the user data stored in a CSV file.
    It offers methods to validate user credentials against the data in the CSV file.
    """

    @staticmethod
    def validate_user(username, password):
        """
        Validates a user's credentials.

        This method opens and reads a CSV file containing user credentials and checks
        if there's a match for the given username and password. It returns True if
        a matching entry is found, otherwise False.

        :param username: The username to be validated.
        :param password: The password to be validated.
        :return: Boolean indicating whether the credentials are valid.
        """
        try:
            # Open the CSV file containing user credentials
            with open('users.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                # Iterate through each row in the CSV file
                for row in reader:
                    # Check if the username and password match the current row
                    if row['username'] == username and row['password'] == password:
                        return True

            # Return False if no match is found
            return False

        except FileNotFoundError:
            # Handle the case where the CSV file doesn't exist
            print("Error: 'users.csv' file not found.")
            return False
