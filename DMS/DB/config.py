import sqlite3
import os
import sys
import logging


if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
    running_mode = "Frozen/executable"
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python main.py')"
    except NameError:
        application_path = os.getcwd()
        running_mode = "Interactive"

dbpath = os.path.join(application_path, "database.db")
query_log_path = os.path.join(application_path, "log_files/queries.log")

logging.basicConfig(filename=query_log_path, filemode='a', level=logging.INFO)

conn = sqlite3.connect(dbpath)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()
conn.set_trace_callback(logging.info)


def create_database():

    plans_table = """
    CREATE TABLE IF NOT EXISTS plans (
        planID INTEGER PRIMARY KEY,
        start_date TEXT,
        end_date TEXT,
        name TEXT,
        region TEXT,
        event_name TEXT,
        description TEXT
        )
        """

    cursor.execute(plans_table)

    camps_table = """
    CREATE TABLE IF NOT EXISTS camps (
        campID INTEGER PRIMARY KEY,
        location TEXT,
        max_shelter INTEGER,
        water INTEGER,
        max_water INTEGER,
        food INTEGER,
        max_food INTEGER,
        medical_supplies INTEGER,
        max_medical_supplies INTEGER,
        planID INTEGER NOT NULL,
        FOREIGN KEY (planID) REFERENCES plans(planID) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """

    cursor.execute(camps_table)

    volunteers_table = """
    CREATE TABLE IF NOT EXISTS volunteers(
        volunteerID INTEGER PRIMARY KEY,
        first_name TEXT, 
        last_name TEXT,
        username TEXT UNIQUE,
        password TEXT,
        date_of_birth TEXT,
        phone TEXT,
        account_status TEXT CHECK (account_status IN ('Admin', 'Active', 'Inactive')),
        campID INTEGER,
        FOREIGN KEY (campID) REFERENCES camps(campID) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """

    cursor.execute(volunteers_table)

    refugees_table = """
    CREATE TABLE IF NOT EXISTS refugees (
        refugeeID INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        date_of_birth TEXT,
        gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')),
        familyID INTEGER,
        medical_condition TEXT,
        vital_status TEXT CHECK (vital_status IN ('Alive', 'Deceased'))
        campID INTEGER NOT NULL,
        FOREIGN KEY (campID) REFERENCES camps(campID) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """

    cursor.execute(refugees_table)

    countries_table = """
    CREATE TABLE IF NOT EXISTS countries (
        country TEXT PRIMARY KEY)
        """

    conn.commit()


create_database()
