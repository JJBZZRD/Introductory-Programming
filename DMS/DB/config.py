import sqlite3
import os
import sys
import logging

print("Initialising database...")
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
    running_mode = "Frozen/executable"
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python __main__.py')"
    except NameError:
        application_path = os.getcwd()
        running_mode = "Interactive"

dbpath = os.path.join(application_path, "database.db")
query_log_path = os.path.join(application_path, "query.log")

logging.basicConfig(filename=query_log_path, filemode='a', level=logging.INFO,
                    format="%(asctime)s \n%(message)s \n", datefmt='%Y-%m-%d %H:%M:%S')

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
        country TEXT,
        event_name TEXT,
        description TEXT,
        water INTEGER,
        food INTEGER,
        medical_supplies INTEGER,
        shelter INTEGER,
        status TEXT CHECK (status IN ('Active', 'Ended')),
        created_time TEXT
        )
        """

    cursor.execute(plans_table)

    camps_table = """
    CREATE TABLE IF NOT EXISTS camps (
        campID INTEGER PRIMARY KEY,
        location TEXT,
        shelter INTEGER,
        water INTEGER,
        food INTEGER,
        medical_supplies INTEGER,
        planID INTEGER NOT NULL,
        created_time TEXT,
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
        created_time TEXT,
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
        campID INTEGER NOT NULL,
        triage_category TEXT CHECK (triage_category IN ('None', 'Non-Urgent', 'Standard', 'Urgent', 'Very-Urgent', 'Immediate')),
        medical_conditions Text,
        vital_status TEXT CHECK (vital_status IN ('Alive', 'Deceased')),
        created_time TEXT,
        FOREIGN KEY (campID) REFERENCES camps(campID) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """

    cursor.execute(refugees_table)
    countries_table = """
    CREATE TABLE IF NOT EXISTS countries (
        country TEXT PRIMARY KEY)
        """

    cursor.execute(countries_table)

    current_user_table = """
    CREATE TABLE IF NOT EXISTS current_user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        time TEXT
    )
    """

    cursor.execute(current_user_table)

    audit_table = """
    CREATE TABLE IF NOT EXISTS audit (
        auditID INTEGER PRIMARY KEY,
        table_name TEXT,
        recordID INTEGER,
        field_name TEXT,
        old_value TEXT,
        new_value TEXT,
        action TEXT,
        action_time TEXT,
        changed_by TEXT
    )
    """

    cursor.execute(audit_table)

    # family_table = """
    # CREATE TABLE IF NOT EXISTS family(
    #     familyID INTEGER PRIMARY KEY,
    #     family_name TEXT,
    #     lead_family_memberID INTEGER)
    #     """

    # cursor.execute(family_table)

    conn.commit()


def triggers_for_audit_table(table_name, fields, primary_key_field):
    for field in fields:

        cursor.execute(f"""
            CREATE TRIGGER IF NOT EXISTS {table_name}_{field}_insert
            AFTER INSERT ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO audit (table_name, recordID, field_name, old_value, new_value, action, action_time, changed_by)
                VALUES ('{table_name}', NEW.{primary_key_field}, '{field}', NULL, NEW.{field}, 'INSERT', CURRENT_TIMESTAMP, (SELECT username FROM current_user ORDER BY id DESC LIMIT 1));
            END;
        """)

        cursor.execute(f"""
            CREATE TRIGGER IF NOT EXISTS {table_name}_{field}_update
            AFTER UPDATE OF {field} ON {table_name}
            FOR EACH ROW
            WHEN OLD.{field} IS NOT NEW.{field}
            BEGIN
                INSERT INTO audit (table_name, recordID, field_name, old_value, new_value, action, action_time, changed_by)
                VALUES ('{table_name}', OLD.{primary_key_field}, '{field}', OLD.{field}, NEW.{field}, 'UPDATE', CURRENT_TIMESTAMP, (SELECT username FROM current_user ORDER BY id DESC LIMIT 1));
            END;
        """)

        cursor.execute(f"""
            CREATE TRIGGER IF NOT EXISTS {table_name}_{field}_delete
            AFTER DELETE ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO audit (table_name, recordID, field_name, old_value, new_value, action, action_time, changed_by)
                VALUES ('{table_name}', OLD.{primary_key_field}, '{field}', OLD.{field}, NULL, 'DELETE', CURRENT_TIMESTAMP, (SELECT username FROM current_user ORDER BY id DESC LIMIT 1));
            END;
        """)

    conn.commit()


plans_fields = ["start_date", "end_date", "name", "country", "event_name", "description", "water", "food",
                "medical_supplies", "shelter", "status"]
camps_fields = ["location", "shelter", "water", "food", "medical_supplies", "planID"]
refugees_fields = ["first_name", "last_name", "date_of_birth", "gender", "familyID", "campID", "triage_category",
                   "medical_conditions", "vital_status"]


def clear_dummy_data():
    for table_name in ["plans", "camps", "volunteers", "refugees", "countries"]:
        q = f"""DELETE FROM {table_name}"""
        cursor.execute(q)
    conn.commit()

def insert_dummy_data():
    plans_data = """
    INSERT INTO plans (planID, start_date, end_date, name, country, event_name, description, shelter, water, food, medical_supplies, status, created_time) VALUES
    (1, '2023-01-01', '2025-01-01', 'Nuclear war', 'United Kingdom', 'Nuclear Crisis Management', 'Nuclear War in England', 100, 100, 100, 100, 'Active', '2023-01-01T14:36:25'),
    (2, '2023-01-01', '2025-01-01', 'London War', 'United Kingdom', 'War', 'Response to war in London', 200, 200, 200, 200, 'Active', '2023-01-01T14:36:25'),
    (3, '2023-01-01', '2025-01-01', 'Paris War', 'France', 'War', 'Response to war in Paris', 300, 300, 300, 300, 'Active', '2023-01-01T14:36:25'),
    (4, '2023-01-01', '2025-01-01', 'War', 'United Kingdom', 'War', 'Response to war in UK', 300, 300, 300, 300, 'Active', '2023-01-01T14:36:25');
    """

    cursor.execute(plans_data)

    camp_data = """
    INSERT INTO camps (campID, location, shelter, water, food, medical_supplies, planID, created_time) VALUES
    (1, 'Camden', 20, 300, 600, 200, 1, '2023-01-01T14:36:25'),
    (2, 'Greenwich', 20, 300, 600, 200, 1, '2023-01-01T14:36:25'),
    (3, 'Snowdonia', 20, 300, 600, 200, 2, '2023-01-01T14:36:25'),
    (4, 'Richmond', 20, 300, 600, 200, 2, '2023-01-01T14:36:25'),
    (5, 'Versailles', 20, 300, 600, 200, 3, '2023-01-01T14:36:25'),
    (6, 'Oxford', 20, 300, 600, 200, 4,'2023-01-01T14:36:25'),
    (7, 'Reading', 20, 300, 600, 200, 4,'2023-01-01T14:36:25');
    """

    cursor.execute(camp_data)

    # Insert dummy data for volunteers
    volunteers_data = """
    INSERT INTO volunteers (first_name, last_name, username, password, date_of_birth, phone, account_status, campID, created_time) VALUES
    -- Camp 1
    ('admin', '111', 'admin', '111', '1990-05-15', '555-1234', 'Active', NULL, '2023-01-01T14:36:25'),
    ('Jane', 'Smith', 'volunteer1', '111', '1985-08-22', '555-5678', 'Active', 1, '2023-01-01T14:36:25'),
    ('Robert', 'Johnson', 'volunteer12', '111', '1992-03-10', '555-9876', 'Active', 1, '2023-01-01T14:36:25'),
    ('Emily', 'Williams', 'volunteer31', '111', '1988-11-27', '555-4321', 'Active', 1, '2023-01-01T14:36:25'),
    ('Michael', 'Brown', 'volunteer6', '111', '1995-07-18', '555-8765', 'Inactive', 1, '2023-01-01T14:36:25'),
    ('Sophia', 'Davis', 'volunteer7', '111', '1993-09-05', '555-2345', 'Active', 1, '2023-01-01T14:36:25'),
    ('David', 'Anderson', 'volunteer8', '111', '1991-02-14', '555-6789', 'Inactive', 1, '2023-01-01T14:36:25'),
    ('Olivia', 'Thomas', 'volunteer9', '111', '1986-12-03', '555-8765', 'Active', 1, '2023-01-01T14:36:25'),
    ('Christopher', 'Garcia', 'volunteer10', '111', '1994-04-20', '555-2345', 'Active', 1, '2023-01-01T14:36:25'),
    ('Emma', 'Johnson', 'volunteer11', '111', '1998-06-08', '555-5678', 'Active', 1, '2023-01-01T14:36:25'),

    -- Camp 2
    ('Daniel', 'White', 'volunteer2', '111', '1987-10-12', '555-3456', 'Active', 2, '2023-01-01T14:36:25'),
    ('Sophie', 'Miller', 'volunteer21', '111', '1994-01-25', '555-7890', 'Active', 2, '2023-01-01T14:36:25'),
    ('Matthew', 'Davis', 'volunteer13', '111', '1990-09-30', '555-2345', 'Active', 2, '2023-01-01T14:36:25'),
    ('Ava', 'Wilson', 'volunteer14', '111', '1985-12-15', '555-6789', 'Active', 2, '2023-01-01T14:36:25'),
    ('Nicholas', 'Taylor', 'volunteer15', '111', '1992-05-18', '555-8765', 'Inactive', 2, '2023-01-01T14:36:25'),
    ('Grace', 'Moore', 'volunteer16', '111', '1997-03-22', '555-1234', 'Active', 2, '2023-01-01T14:36:25'),
    ('Ethan', 'Baker', 'volunteer17', '111', '1988-08-08', '555-5678', 'Inactive', 2, '2023-01-01T14:36:25'),
    ('Chloe', 'Fisher', 'volunteer18', '111', '1995-04-02', '555-2345', 'Active', 2, '2023-01-01T14:36:25'),
    ('Caleb', 'Ward', 'volunteer19', '111', '1989-11-10', '555-6789', 'Active', 2, '2023-01-01T14:36:25'),
    ('Madison', 'Perry', 'volunteer20', '111', '1996-07-17', '555-8765', 'Active', 2, '2023-01-01T14:36:25'),

    -- Camp 3
    ('Liam', 'Carter', 'volunteer3', '111', '1993-02-05', '555-2345', 'Active', 3, '2023-01-01T14:36:25'),
    ('Aubrey', 'Hayes', 'volunteer30', '111', '1998-08-20', '555-6789', 'Active', 3, '2023-01-01T14:36:25'),
    ('Mason', 'Wells', 'volunteer22', '111', '1991-04-15', '555-1234', 'Active', 3, '2023-01-01T14:36:25'),
    ('Harper', 'Barnes', 'volunteer23', '111', '1986-10-30', '555-5678', 'Active', 3, '2023-01-01T14:36:25'),
    ('Aiden', 'Fisher', 'volunteer24', '111', '1994-12-22', '555-8765', 'Inactive', 3, '2023-01-01T14:36:25'),
    ('Ella', 'Bryant', 'volunteer25', '111', '1997-06-18', '555-2345', 'Active', 3, '2023-01-01T14:36:25'),
    ('Logan', 'Coleman', 'volunteer26', '111', '1989-01-12', '555-6789', 'Inactive', 3, '2023-01-01T14:36:25'),
    ('Avery', 'Reyes', 'volunteer27', '111', '1996-03-25', '555-8765', 'Active', 3, '2023-01-01T14:36:25'),
    ('Lucas', 'Scott', 'volunteer28', '111', '1992-07-08', '555-2345', 'Active', 3, '2023-01-01T14:36:25'),
    ('Sophie', 'Jordan', 'volunteer29', '111', '1995-09-20', '555-6789', 'Active', 3, '2023-01-01T14:36:25'),
    
    -- Camp 6
    ('Cuthbert', 'Jones', 'volunteer4', '111', '1996-01-16', '555-6789', 'Active', 6, '2023-01-01T14:36:25'),
    
    -- Camp 7
    ('Penelope', 'Walsh', 'volunteer5', '111', '1980-09-07', '555-2345', 'Active', 7, '2023-01-01T14:36:25')
    """

    cursor.execute(volunteers_data)

    refugees_data = """
    INSERT INTO refugees (first_name, last_name, date_of_birth, gender, familyID, campID, triage_category, medical_conditions, vital_status, created_time) VALUES

    --Family separated: 8, 10, 

    -- Camp 1
    ('Isabella', 'Johnson', '2002-08-10', 'Female', 1, 1, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Smith', '1980-03-25', 'Male', 2, 1, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Charlotte', 'Taylor', '1995-12-05', 'Female', 3, 1, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Henry', 'Clark', '2010-05-18', 'Male', 4, 1, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophia', 'Williams', '1998-10-30', 'Female', 5, 1, 'Urgent', 'Respiratory Infection', 'Alive', '2023-01-01T14:36:25'),
    ('Jacob', 'Brown', '2014-06-22', 'Male', 6, 1, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Amelia', 'Harrison', '2003-04-03', 'Female', 7, 1, 'Non-Urgent', 'Allergies', 'Alive', '2023-01-01T14:36:25'),
    ('William', 'Baker', '1990-01-12', 'Male', 8, 1, 'None', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    ('Sophie', 'Evans', '2005-09-20', 'Female', 9, 1, 'Urgent', 'Heart Disease', 'Alive', '2023-01-01T14:36:25'),
    ('Thomas', 'Jones', '1988-07-08', 'Male', 10, 1, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Aisha', 'Khan', '1996-06-18', 'Female', 11, 1, 'Urgent', 'Hypertension', 'Alive', '2023-01-01T14:36:25'),
    ('Alexander', 'Brown', '1983-08-14', 'Male', 12, 1, 'None', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Lily', 'Taylor', '2007-11-02', 'Female', 13, 1, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Daniel', 'Evans', '2000-02-25', 'Male', 9, 1, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ella', 'Williams', '1993-03-12', 'Female', 15, 1, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Leo', 'Jones', '2012-12-30', 'Male', 10, 1, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Zara', 'Clark', '2005-07-28', 'Female', 17, 1, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'Evans', '1998-04-15', 'Female', 9, 1, 'Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Nooh', 'Baker', '2011-09-10', 'Male', 8, 1, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Liam', 'Thompson', '2004-05-05', 'Male', 20, 1, 'None', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),

    -- Camp 2
    ('Emily', 'White', '2001-11-10', 'Female', 21, 2, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Alexander', 'Miller', '1995-03-25', 'Male', 22, 2, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'Davis', '2008-12-05', 'Female', 23, 2, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Leo', 'Baker', '2012-05-18', 'Male', 8, 2, 'Immediate', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Isabella', 'Clark', '1999-09-30', 'Female', 25, 2, 'Urgent', 'Respiratory Infection', 'Alive', '2023-01-01T14:36:25'),
    ('James', 'Martin', '2007-11-15', 'Male', 26, 2, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Poppy', 'Harrison', '2015-04-03', 'Female', 7, 2, 'Non-Urgent', 'Allergies', 'Alive', '2023-01-01T14:36:25'),
    ('Jack', 'Baker', '1988-06-22', 'Male', 8, 2, 'Immediate', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    ('Ruby', 'Evans', '2003-09-20', 'Female', 29, 2, 'Urgent', 'Heart Disease', 'Alive', '2023-01-01T14:36:25'),
    ('George', 'Jones', '1994-07-08', 'Male', 10, 2, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophie', 'Harrison', '1996-06-18', 'Female', 7, 2, 'Urgent', 'Hypertension', 'Alive', '2023-01-01T14:36:25'),
    ('Benjamin', 'Hill', '1983-08-14', 'Male', 32, 2, 'Immediate', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Isla', 'Clark', '2007-11-02', 'Female', 33, 2, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Jacob', 'Evans', '2000-02-25', 'Male', 29, 2, 'Immediate', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ella', 'Williams', '1993-03-12', 'Female', 35, 2, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Jones', '2012-12-30', 'Male', 10, 2, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Zara', 'Clark', '2005-07-28', 'Female', 37, 2, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ava', 'Evans', '1998-04-15', 'Female', 29, 2, 'Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Noah', 'Baker', '2011-09-10', 'Male', 39, 2, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ethan', 'Thompson', '2004-05-05', 'Male', 40, 2, 'Immediate', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),

    -- Camp 3
    ('Lily', 'White', '1996-04-20', 'Female', 41, 3, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Taylor', '2002-08-15', 'Male', 42, 3, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Ava', 'Harrison', '2010-10-05', 'Female', 7, 3, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Ethan', 'Baker', '2014-11-18', 'Male', 39, 3, 'Immediate', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'Williams', '2001-09-30', 'Female', 45, 3, 'Urgent', 'Respiratory Infection', 'Alive', '2023-01-01T14:36:25'),
    ('Noah', 'Martin', '2012-01-15', 'Male', 46, 3, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Layla', 'Harrison', '2015-04-02', 'Female', 7, 3, 'Non-Urgent', 'Allergies', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Baker', '1998-01-12', 'Male', 39, 3, 'Immediate', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    ('Isla', 'Evans', '2005-09-20', 'Female', 49, 3, 'Urgent', 'Heart Disease', 'Alive', '2023-01-01T14:36:25'),
    ('Harry', 'Jones', '1992-07-08', 'Male', 10, 3, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophia', 'Taylor', '1996-06-18', 'Female', 51, 3, 'Urgent', 'Hypertension', 'Alive', '2023-01-01T14:36:25'),
    ('Henry', 'Hill', '1983-08-14', 'Male', 52, 3, 'Immediate', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Eva', 'Clark', '2007-11-02', 'Female', 53, 3, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Daniel', 'Evans', '2000-02-25', 'Male', 49, 3, 'Immediate', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophie', 'Williams', '1993-03-12', 'Female', 55, 3, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Leo', 'Jones', '2012-12-30', 'Male', 10, 3, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Zara', 'Clark', '2005-07-28', 'Female', 57, 3, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'Evans', '1998-04-15', 'Female', 49, 3, 'Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Noah', 'Baker', '2011-09-10', 'Male', 8, 3, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ella', 'Thompson', '2004-05-05', 'Male', 60, 3, 'Immediate', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    
    -- Camp 6
    ('Phoebe', 'Taylor', '1998-02-19', 'Female', 61, 6, 'Immediate', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Edward', 'Moldoon', '1983-08-14', 'Male', 62, 6, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    
    -- Camp 7
    ('Timothy', 'Wright', '1980-08-19', 'Male', 63, 7, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Victoria', 'Clack', '1970-09-23', 'Female', 64, 7, 'None', 'None', 'Alive', '2023-01-01T14:36:25')
    """

    cursor.execute(refugees_data)

    insert_countries = """
    INSERT INTO countries (country) VALUES
    ("Afghanistan"), ("Albania"), ("Algeria"), ("Andorra"), ("Angola"), ("Antigua and Barbuda"), ("Argentina"),
    ("Armenia"), ("Australia"), ("Austria"), ("Azerbaijan"), ("Bahamas"), ("Bahrain"), ("Bangladesh"), ("Barbados"),
    ("Belarus"), ("Belgium"), ("Belize"), ("Benin"), ("Bhutan"), ("Bolivia"), ("Bosnia and Herzegovina"), ("Botswana"),
    ("Brazil"), ("Brunei"), ("Bulgaria"), ("Burkina Faso"), ("Burundi"), ("Côte d'Ivoire"), ("Cabo Verde"), ("Cambodia"),
    ("Cameroon"), ("Canada"), ("Central African Republic"), ("Chad"), ("Chile"), ("China"), ("Colombia"), ("Comoros"),
    ("Congo (Congo-Brazzaville)"), ("Costa Rica"), ("Croatia"), ("Cuba"), ("Cyprus"), ("Czechia (Czech Republic)"),
    ("Democratic Republic of the Congo"), ("Denmark"), ("Djibouti"), ("Dominica"), ("Dominican Republic"), ("Ecuador"),
    ("Egypt"), ("El Salvador"), ("Equatorial Guinea"), ("Eritrea"), ("Estonia"), ("Eswatini (Swaziland)"), ("Ethiopia"),
    ("Fiji"), ("Finland"), ("France"), ("Gabon"), ("Gambia"), ("Georgia"), ("Germany"), ("Ghana"), ("Greece"), ("Grenada"),
    ("Guatemala"), ("Guinea"), ("Guinea-Bissau"), ("Guyana"), ("Haiti"), ("Holy See (Vatican City State)"), ("Honduras"),
    ("Hungary"), ("Iceland"), ("India"), ("Indonesia"), ("Iran"), ("Iraq"), ("Ireland"), ("Israel"), ("Italy"), ("Jamaica"),
    ("Japan"), ("Jordan"), ("Kazakhstan"), ("Kenya"), ("Kiribati"), ("Kuwait"), ("Kyrgyzstan"), ("Laos"), ("Latvia"), ("Lebanon"),
    ("Lesotho"), ("Liberia"), ("Libya"), ("Liechtenstein"), ("Lithuania"), ("Luxembourg"), ("Madagascar"), ("Malawi"),
    ("Malaysia"), ("Maldives"), ("Mali"), ("Malta"), ("Marshall Islands"), ("Mauritania"), ("Mauritius"), ("Mexico"),
    ("Micronesia"), ("Moldova"), ("Monaco"), ("Mongolia"), ("Montenegro"), ("Morocco"), ("Mozambique"), ("Myanmar"),
    ("Namibia"), ("Nauru"), ("Nepal"), ("Netherlands"), ("New Zealand"), ("Nicaragua"), ("Niger"), ("Nigeria"), ("North Korea"),
    ("North Macedonia"), ("Norway"), ("Oman"), ("Pakistan"), ("Palau"), ("Palestine (State of)"), ("Panama"), ("Papua New Guinea"),
    ("Paraguay"), ("Peru"), ("Philippines"), ("Poland"), ("Portugal"), ("Qatar"), ("Romania"), ("Russia"), ("Rwanda"),
    ("Saint Kitts and Nevis"),
    ("Saint Lucia"), ("Saint Vincent and the Grenadines"), ("Samoa"), ("San Marino"), ("Sao Tome and Principe"), ("Saudi Arabia"),
    ("Senegal"), ("Serbia"), ("Seychelles"), ("Sierra Leone"), ("Singapore"), ("Slovakia"), ("Slovenia"), ("Solomon Islands"),
    ("Somalia"),
    ("South Africa"), ("South Korea"), ("South Sudan"), ("Spain"), ("Sri Lanka"), ("Sudan"), ("Suriname"), ("Sweden"), ("Switzerland"),
    ("Syria"), ("Tajikistan"), ("Tanzania"), ("Thailand"), ("Timor-Leste"), ("Togo"), ("Tonga"), ("Trinidad and Tobago"), ("Tunisia"),
    ("Turkey"), ("Turkmenistan"), ("Tuvalu"), ("Uganda"), ("Ukraine"), ("United Arab Emirates"), ("United Kingdom"), ("United States"),
    ("Uruguay"), ("Uzbekistan"), ("Vanuatu"), ("Venezuela"), ("Vietnam"), ("Yemen"), ("Zambia"), ("Zimbabwe");
    """

    cursor.execute(insert_countries)

    cursor.execute("""
    INSERT INTO current_user (id, username) VALUES (1, 'default_user')
    ON CONFLICT(id) DO UPDATE SET username = 'default_user';
    """)

    conn.commit()


def check_sample_db_init():
    cursor.execute("SELECT * FROM volunteers WHERE username = 'admin' and password = '111'")
    return cursor.fetchone() is None


create_database()

triggers_for_audit_table("plans", plans_fields, "planID")
triggers_for_audit_table("camps", camps_fields, "campID")
triggers_for_audit_table("refugees", refugees_fields, "refugeeID")

if __name__ == "__main__" or check_sample_db_init():
    print("Inserting dummy data...")
    clear_dummy_data()
    insert_dummy_data()