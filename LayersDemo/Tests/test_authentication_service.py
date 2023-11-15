import unittest
from unittest.mock import patch
from BusinessLogicLayer.authentication_service import AuthenticationService

class TestAuthenticationService(unittest.TestCase):
    """
    TestAuthenticationService contains unit tests for the AuthenticationService class.
    It uses mocking to isolate the tests from the actual data layer.
    """

    @patch('DataAccessLayer.user_data_access.UserDataAccess.validate_user')
    def test_authenticate_valid(self, mock_validate_user):
        """
        Test to ensure authenticate method returns True for valid credentials.

        This test mocks the validate_user method from UserDataAccess to simulate
        a scenario where the provided credentials are valid. It then checks if
        the authenticate method correctly recognizes them as valid.

        :param mock_validate_user: Mocked instance of the validate_user method.
        """
        # Setup the mock to return True for a specific set of credentials
        mock_validate_user.return_value = True

        # Call the authenticate method with the credentials
        result = AuthenticationService.authenticate("valid_user", "valid_password")

        # Assert that the result is True
        self.assertTrue(result)

    @patch('DataAccessLayer.user_data_access.UserDataAccess.validate_user')
    def test_authenticate_invalid(self, mock_validate_user):
        """
        Test to ensure authenticate method returns False for invalid credentials.

        This test mocks the validate_user method from UserDataAccess to simulate
        a scenario where the provided credentials are invalid. It then checks if
        the authenticate method correctly recognizes them as invalid.

        :param mock_validate_user: Mocked instance of the validate_user method.
        """
        # Setup the mock to return False for a specific set of credentials
        mock_validate_user.return_value = False

        # Call the authenticate method with the credentials
        result = AuthenticationService.authenticate("invalid_user", "invalid_password")

        # Assert that the result is False
        self.assertFalse(result)

# This allows the test cases to be executed
if __name__ == '__main__':
    unittest.main()
