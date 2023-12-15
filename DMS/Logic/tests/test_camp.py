import unittest
import sqlite3
from ...DB.camp import Camp
from ...DB.plan import Plan
from ..camp_data_retrieve import CampDataRetrieve
from ..camp_data_edit import CampDataEdit
from ...DB.config import *


class TestCamp(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
        print(" ========================= Setting up resources for the test ======================== ")
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        create_database()

    def tearDown(self) -> None:
        print("Tearing down resources after the test")
        self.connection.close()

    # def test_create_camp(self):
    #     print("\nExecuting test_create_camp")

    #     camp_a = CampDataEdit.create_camp('a', 50, None, 50, None, 50, None, 50, 10)

    #     self.assertIsInstance(camp_a, list, "camp_a is not a list")

    #     pass

    def test_update_camp(self):
        print("\nExecuting update_camp")

        camp_b = CampDataEdit.update_camp(1, location='Australia')

        self.assertIsInstance(camp_b, list, "camp_b is not a list")

    def test_get_all_camp(self):
        print("\nExecuting get_all_camps")
    
        camp_c = CampDataRetrieve.get_all_camps()
        for camp in camp_c:
            print(camp.display_info())
    
        self.assertIsInstance(camp_c, list, "camp_c is not a list")

    def test_get_camp(self):
        print("\nExecuting get_camp")

        camp_d = CampDataRetrieve.get_camp(campID=1)

        self.assertIsInstance(camp_d, list, "camp_d is not a list")

    def test_get_camp_blank(self):
        print("\nExecuting get_camp with blank")

        camp_e = CampDataRetrieve.get_camp(campID=1, location='China')

        self.assertIsInstance(camp_e, list, "camp_e is not a list")

    def test_get_camp_resources(self):
        print("\n --------------------------- Executing get_camp_resources ---------------------")

        resources = CampDataRetrieve.get_camp_resources(campID=1)
        print(resources)

        self.assertIsInstance(resources, dict, "resources is not a dict")

    def test_get_stats_triage_category(self):
        print(" ------------ Executing test_get_stats_triage_category --------------- ")
        # print(CampDataRetrieve.get_stats_triage_category(1))
        res = CampDataRetrieve.get_stats_triage_category(1)
        self.assertIsInstance(res, dict, 'res is not a dict')

    def test_get_stats_gender(self):
        print(" ------------ Executing test_get_stats_gender --------------- ")
        print(CampDataRetrieve.get_stats_gender(1))
        res = CampDataRetrieve.get_stats_gender(1)
        self.assertIsInstance(res, dict, 'res is not a dict')

    def test_get_stats_family(self):
        print(" ------------ Executing test_get_stats_family --------------- ")
        print(CampDataRetrieve.get_stats_family(1))
        res = CampDataRetrieve.get_stats_family(1)
        self.assertIsInstance(res, dict, 'res is not a dict')



if __name__ == '__main__':
    unittest.main()
