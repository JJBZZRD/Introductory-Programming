import unittest
import sqlite3
from person_data_retrieve import *
from person_data_edit import *
from config import *
from camp import *
from plan import *
import util

class TestVolunteer(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
        print("=============================================================")
        print("Setting up resources for the test")
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        create_database()
        sql = """
            INSERT INTO plans (start_date, name) 
            VALUES ('2023-01-01', 'soran unit test plan');
        """
        sql2 = """
            INSERT INTO camps (planID)
            VALUES ((SELECT planID from plans WHERE name = 'soran unit test plan'));
        """
        cursor.execute(sql)
        cursor.execute(sql2)
        # conn.commit()
        camp_id = cursor.execute("SELECT last_insert_rowid() from camps").fetchone()[0]
        camp_tuple = Camp.get_camp_by_id(camp_id)
        camp = util.parse_result('Camp', camp_tuple)[0]
        print(f'Camp created: {camp.display_info()}')

    def tearDown(self):
        print("Tearing down resources after the test")
        self.connection.rollback()
        self.connection.close()

    def test_create_volunteer_admin(self):
        print(" ---------------- Executing test_create_volunteer_admin -------------- ")

        admins = PersonDataRetrieve.get_volunteers(username='admin')
        if admins:
            print(admins[0].display_info())
            self.assertIsInstance(admins, list, f'Admins is not a list but {admins}')
        # else:
        #     admin = PersonDataEdit.create_volunteer('admin', 'test', 'admin', '111', '2023-1-1', '10123456', 'Active', )
        
        # self.assertIsInstance(vols, list, 'vols is not a list')
        pass

    def test_get_all_volunteers(self):
        volunteers = PersonDataRetrieve.get_all_volunteers()
        # for v in volunteers:
        #     print(v.display_info())
        self.assertIsInstance(volunteers, list, 'get_all_volunteers FAILED')

    def test_get_volutneer(self):
        print(" ------------ Executing test_get_volutneer --------------- ")
        vols = PersonDataRetrieve.get_volunteers(username='volunteer1', password='111', account_status='Active')
        print(vols[0].display_info())
        self.assertIsInstance(vols, list, "get_volunteers(campID='') FAILED")

    def test_get_volunteer_admin(self):
        print(" ------------ Executing test_get_volunteer_admin --------------- ")
        admins = PersonDataRetrieve.get_volunteers(name='Admin')
        # print(f'admins: {admins}')
        self.assertIsInstance(admins, list, f'Admins is not a list but {admins}')

    def test_update_volunteer_status(self):
        print(" ------------ Executing test_update_volunteer_status --------------- ")
        admin = PersonDataRetrieve.get_volunteers(username='admin')[0]
        admin = PersonDataEdit.update_volunteer(admin.volunteerID, account_status='Active')[0]
        print(admin)
        print(admin.display_info())

if __name__ == '__main__':
    unittest.main()