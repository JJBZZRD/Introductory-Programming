import unittest
import sqlite3
from ..person_data_retrieve import *
from ..person_data_edit import *
from ..plan_data_retrieve import *
from ..plan_data_edit import *
from ...DB.config import *
from ...DB.camp import *
from ...DB.plan import *
from ... import util


class TestPlan(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
        print("Setting up resources for the test")
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        create_database()

    def tearDown(self) -> None:
        print("Tearing down resources after the test")
        self.connection.close()

    def test_get_all_plans(self):
        plans = PlanDataRetrieve.get_all_plans()
        self.assertIsInstance(plans, list, 'Get_all_plans FAILED')
    
    def test_get_plan(self):
        print(" \n------------ Executing test_get_plan --------------- ")
        plan = PlanDataRetrieve.get_plan(planID=1, country='United Kingdom')
        self.assertIsInstance(plan, list, 'Get_plan FAILED')
        
    def test_get_resources(self):
        print(" \n------------ Executing test_get_resources --------------- ")
        
        resources = PlanDataRetrieve.get_resources(1)
        print(f"resource: {resources}")
        self.assertEqual(len(resources), 4, 'test_get_resources does not return 4 resources')

    def test_get_plan_resources_estimation(self):
        print(" \n------------ Executing test_get_resources_estimation --------------- ")

        estimation = PlanDataRetrieve.get_plan_resources_estimate(planID=1)
        print(f"estimation: {estimation}")
        self.assertEqual(len(estimation), 3, 'test_get_resources_estimation FAILED')        

    def test_create_plan(self):
        print(" \n------------ Executing test_create_plan --------------- ")

        plan = PlanEdit.create_plan(name='asdf', event_name='uvuib', country='United Kingdom',
                                    description='Nuclear', start_date='2023-01-01', end_date='2024-01-01')
        self.assertIsNotNone(plan, 'Create_plan returned None')
      
    def test_update_plan(self):
        print(" \n------------ Executing test_update_plan --------------- ")
        plan = PlanEdit.update_plan(planID=1, country='United Kingdom')
        print(plan)
        self.assertIsInstance(plan, list, 'Update_plan FAILED')        

    def test_get_stats_triage_category(self):
        print(" ------------ Executing test_get_stats_triage_category --------------- ")
        stats = PlanDataRetrieve.get_stats_triage_category(1)
        print(f'stats: {stats}')
        self.assertEqual(len(stats), 12, 'get_stats_triage_category should return 12 figures')

    def test_get_stats_gender(self):
        print(" ------------ Executing test_get_stats_gender --------------- ")
        stats = PlanDataRetrieve.get_stats_gender(1)
        print(f'stats: {stats}')
        self.assertEqual(len(stats), 6, 'get_stats_gender should return 6 figures')

    def test_get_stats_age(self):
        print(" ------------ Executing test_get_stats_triage_category --------------- ")
        stats = PlanDataRetrieve.get_stats_age(1)
        print(f'stats: {stats}')
        self.assertEqual(len(stats), 6, 'test_get_stats_age should return 6 figures')

    def test_get_stats_family(self):
        print(" ------------ Executing test_get_stats_family --------------- ")
        stats = PlanDataRetrieve.get_stats_family(1)
        print(f'stats: {stats}')
        self.assertEqual(len(stats), 2, 'get_stats_family should return 2 figures')       
 
    def test_get_stats_vital_status(self):
        print(" ------------ Executing test_get_stats_vital_status --------------- ")
        stats = PlanDataRetrieve.get_stats_vital_status(1)
        print(f'stats: {stats}')
        self.assertEqual(len(stats), 4, 'get_stats_vital_status should return 4 figures')
    # def test_delete_plan(self):
    #     plan = PlanEdit.delete_plan(planID=1)
    #     print(plan)





if __name__ == '__main__':
    unittest.main()