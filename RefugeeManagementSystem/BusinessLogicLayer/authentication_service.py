# Import the UserDataAccess class from the DataAccessLayer package

class AuthenticationService:
    """
    AuthenticationService provides the business logic for authenticating users.
    It interfaces with the UserDataAccess class to validate user credentials.
    """

    @staticmethod
    def login(username, password):
        """
        Authenticates a user based on the provided username and password.

        This method uses the UserDataAccess class to validate the user's credentials.
        It returns True if the credentials are valid, otherwise False.

        :param username: The username of the user trying to log in.
        :param password: The password of the user trying to log in.
        :return: Boolean indicating the result of the authentication process.
        """
        # Validate the user's credentials using the UserDataAccess class
        pass
    # @staticmethod
    # def logout():
    #     return "login_page"


    @staticmethod
    def redirect(self, user):
        # user = UserDataAccess.get_user(username, password)
        if user.type == "Admin":
            return "admin_main_page"
        else:
            return "volunteer_main_page"
        
        