import unittest
import sqlite3
from .person_data_retrieve import *
from .person_data_edit import *
from ..DB.config import *
from ..DB.camp import *
from ..DB.plan import *
from .. import util

class TestVolunteer(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
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
        camp_id = cursor.execute("SELECT last_insert_rowid() FROM camps").fetchone()[0]
        camp_tuple = Camp.get_camp_by_id(camp_id)
        camp = util.parse_result('Camp', camp_tuple)[0]
        print(camp.display_info())

    def tearDown(self):
        print("Tearing down resources after the test")
        self.connection.rollback()
        self.connection.close()

    def test_create_volunteer(self):
        print("Executing test_create_volunteer")

        # vols = PersonDataEdit.create_volunteer('unit test first name', 'unit test last name', '28', 'username', 'password', '2023-1-1', '10123456')
        
        # self.assertIsInstance(vols, list, 'vols is not a list')
        pass

if __name__ == '__main__':
    unittest.main()