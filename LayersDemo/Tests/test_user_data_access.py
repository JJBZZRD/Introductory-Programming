import unittest
from unittest.mock import patch, mock_open
from DataAccessLayer.user_data_access import UserDataAccess

class TestUserDataAccess(unittest.TestCase):
    """
    TestUserDataAccess contains unit tests for the UserDataAccess class.
    It uses mocking to simulate the behavior of reading from a CSV file.
    """

    @patch("builtins.open", new_callable=mock_open, read_data="username,password\nadmin,admin\n")
    def test_validate_user_valid(self, mock_file):
        """
        Test to ensure validate_user returns True for valid credentials.

        This test mocks the open function to simulate reading from a CSV file.
        The mock CSV contains a username and password pair. The test checks if
        validate_user correctly identifies valid credentials.

        :param mock_file: Mocked instance of the open function.
        """
        # Call the validate_user method with valid credentials
        result = UserDataAccess.validate_user("admin", "admin")

        # Assert that the result is True for valid credentials
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open, read_data="username,password\nadmin,admin\n")
    def test_validate_user_invalid(self, mock_file):
        """
        Test to ensure validate_user returns False for invalid credentials.

        This test mocks the open function to simulate reading from a CSV file.
        It checks if validate_user correctly identifies invalid credentials.

        :param mock_file: Mocked instance of the open function.
        """
        # Call the validate_user method with invalid credentials
        result = UserDataAccess.validate_user("admin", "wrongpassword")

        # Assert that the result is False for invalid credentials
        self.assertFalse(result)

# This allows the test cases to be executed
if __name__ == '__main__':
    unittest.main()
