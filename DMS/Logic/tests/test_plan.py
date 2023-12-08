import unittest
import sqlite3
from ..person_data_retrieve import *
from ..person_data_edit import *
from ..plan_data_retrieve import *
from ..plan_data_edit import *
from ...DB.config import *
from ...DB.camp import *
from ...DB.plan import *


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

    def test_get_plan()


if __name__ == '__main__':
    unittest.main()