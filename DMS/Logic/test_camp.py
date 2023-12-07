import os
import sys

CURRENT_DIR = os.path.dirname(
    os.path.abspath(r"path of config"))
sys.path.append(CURRENT_DIR)
import unittest
import sqlite3
from camp_data_retrieve import CampDataRetrieve
from camp_data_edit import CampDataEdit
from DataLayer.plan import Plan
from DataLayer.camp import Camp
from util import *
from DataLayer.config import *


class TestCamp(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
        print("Setting up resources for the test")
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        create_database()

    def tearDown(self) -> None:
        print("Tearing down resources after the test")
        self.connection.close()

    def test_create_camp(self):
        print("\nExecuting test_create_camp")

        camp_a = CampDataEdit.create_camp('a', 50, None, 50, None, 50, None, 50, 10)

        self.assertIsInstance(camp_a, list, "camp_a is not a list")

        pass

    def test_update_camp(self):
        print("\nExecuting update_camp")

        camp_b = CampDataEdit.update_camp(1, location='Australia')

        self.assertIsInstance(camp_b, list, "camp_b is not a list")

        pass

    # def test_get_all_camp(self):
    #     print("\nExecuting get_all_camps")
    #
    #     camp_c = CampDataRetrieve.get_all_camps()
    #
    #     self.assertIsInstance(camp_c, list, "camp_c is not a list")
    #
    #     pass

    def test_get_camp(self):
        print("\nExecuting get_camp")

        camp_d = CampDataRetrieve.get_camp(campID=1)

        self.assertIsInstance(camp_d, list, "camp_d is not a list")

        pass

    def test_get_camp_blank(self):
        print("\nExecuting get_camp with blank")

        camp_e = CampDataRetrieve.get_camp(campID=1, location='China')

        self.assertIsInstance(camp_e, list, "camp_e is not a list")

        pass


if __name__ == '__main__':
    unittest.main()
