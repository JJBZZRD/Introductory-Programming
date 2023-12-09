import unittest
import sqlite3
from ..person_data_retrieve import *
from ..person_data_edit import *
from ..camp_data_retrieve import *
from ..plan_data_retrieve import *
from ...DB.config import *
from ...DB.camp import *
from ...DB.plan import *
from ... import util

class test_db(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
        print("Setting up resources for the test")
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        create_database()
        # sql = """
        #     INSERT INTO plans (start_date, name) 
        #     VALUES ('2023-01-01', 'soran unit test plan');
        # """
        # sql2 = """
        #     INSERT INTO camps (planID)
        #     VALUES ((SELECT planID from plans WHERE name = 'soran unit test plan'));
        # """
        # cursor.execute(sql)
        # cursor.execute(sql2)
        # # conn.commit()
        # camp_id = cursor.execute("SELECT last_insert_rowid() FROM camps").fetchone()[0]
        # camp_tuple = Camp.get_camp_by_id(camp_id)
        # camp = util.parse_result('Camp', camp_tuple)[0]
        # print(camp.display_info())
        # sql3 = f"""
        # INSERT INTO refugees (campID, first_name, last_name, date_of_birth)
        # VALUES({camp_id}, 'aaa', 'bbb', '1111-11-11')
        # """
        # cursor.execute(sql3)

    def tearDown(self):
        print("Tearing down resources after the test")
        self.connection.rollback()
        self.connection.close()

    # def test_insert_admin(self):
    #     q = """
    #     INSERT INTO volunteers(first_name, last_name, username, password, account_status)
    #     VALUES ('admin', 'test', 'admin', '111', 'Admin')
    #     """
    #     cursor.execute(q)

    # def test_get_volunteers(self):
    #     print("Executing test_create_volunteer")
    #     # print(Volunteer.get_all_volunteers())
    #     persons = PersonDataRetrieve.get_all_volunteers()

    # def test_update_volunteer(self):
    #     print(" ------------ Executing test_update_volunteer_status --------------- ")
    #     res = Volunteer.update_volunteer(31, account_status='Active')
    #     print(res)

    def test_get_separate_family_by_camp(self):
        # print(Camp.get_separate_family_by_camp(2))
        # print(Camp.get_separate_family_by_plan(1))
        print(Camp.get_separate_family())
        print(Camp.get_camp_families(1))
if __name__ == '__main__':
    unittest.main()