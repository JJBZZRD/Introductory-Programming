import unittest
import sqlite3
from person_data_retrieve import *
from person_data_edit import *
from camp_data_retrieve import *
from plan_data_retrieve import *
from config import *
from camp import *
from plan import *
import util

class TestVolunteer(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
        print("Setting up resources for the test")
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        # config.create_database()
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
        print(camp.display_info())
        sql3 = f"""
        INSERT INTO refugees (campID, first_name, last_name, date_of_birth)
        VALUES({camp_id}, 'aaa', 'bbb', '1111-11-11')
        """
        cursor.execute(sql3)

    def tearDown(self):
        print("Tearing down resources after the test")
        self.connection.rollback()
        self.connection.close()

    def test_create_volunteer(self):
        print("Executing test_create_volunteer")
        plan = PlanDataRetrieve.get_plan(name='soran unit test plan')[0]
        camp = CampDataRetrieve.get_camp(planID=plan.planID)[0]
        print(camp.display_info())
        refugee = PersonDataRetrieve.get_refugees(camp_id=camp.campID)[0]
        print(refugee.display_info())
        print(Refugee.get_refugee(campID=1))
if __name__ == '__main__':
    unittest.main()