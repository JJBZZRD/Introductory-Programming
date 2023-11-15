# Import the UserDataAccess class from the DataAccessLayer package
from DataAccessLayer.user_data_access import UserDataAccess

class AuthenticationService:
    """
    AuthenticationService provides the business logic for authenticating users.
    It interfaces with the UserDataAccess class to validate user credentials.
    """

    @staticmethod
    def authenticate(username, password):
        """
        Authenticates a user based on the provided username and password.

        This method uses the UserDataAccess class to validate the user's credentials.
        It returns True if the credentials are valid, otherwise False.

        :param username: The username of the user trying to log in.
        :param password: The password of the user trying to log in.
        :return: Boolean indicating the result of the authentication process.
        """
        # Validate the user's credentials using the UserDataAccess class
        return UserDataAccess.validate_user(username, password)
