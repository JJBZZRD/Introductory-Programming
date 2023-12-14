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

logging.basicConfig(
    filename=query_log_path,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s \n%(message)s \n",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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
        account_status TEXT CHECK (account_status IN ('Active', 'Inactive')),
        campID INTEGER,
        created_time TEXT
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
        cursor.execute(
            f"""
            CREATE TRIGGER IF NOT EXISTS {table_name}_{field}_insert
            AFTER INSERT ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO audit (table_name, recordID, field_name, old_value, new_value, action, action_time, changed_by)
                VALUES ('{table_name}', NEW.{primary_key_field}, '{field}', NULL, NEW.{field}, 'INSERT', CURRENT_TIMESTAMP, (SELECT username FROM current_user ORDER BY time DESC LIMIT 1));
            END;
        """
        )

        cursor.execute(
            f"""
            CREATE TRIGGER IF NOT EXISTS {table_name}_{field}_update
            AFTER UPDATE OF {field} ON {table_name}
            FOR EACH ROW
            WHEN OLD.{field} IS NOT NEW.{field}
            BEGIN
                INSERT INTO audit (table_name, recordID, field_name, old_value, new_value, action, action_time, changed_by)
                VALUES ('{table_name}', OLD.{primary_key_field}, '{field}', OLD.{field}, NEW.{field}, 'UPDATE', CURRENT_TIMESTAMP, (SELECT username FROM current_user ORDER BY time DESC LIMIT 1));
            END;
        """
        )

        cursor.execute(
            f"""
            CREATE TRIGGER IF NOT EXISTS {table_name}_{field}_delete
            AFTER DELETE ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO audit (table_name, recordID, field_name, old_value, new_value, action, action_time, changed_by)
                VALUES ('{table_name}', OLD.{primary_key_field}, '{field}', OLD.{field}, NULL, 'DELETE', CURRENT_TIMESTAMP, (SELECT username FROM current_user ORDER BY time DESC LIMIT 1));
            END;
        """
        )

    conn.commit()


plans_fields = [
    "start_date",
    "end_date",
    "name",
    "country",
    "event_name",
    "description",
    "water",
    "food",
    "medical_supplies",
    "shelter",
    "status",
]
camps_fields = ["location", "shelter", "water", "food", "medical_supplies", "planID"]
refugees_fields = [
    "first_name",
    "last_name",
    "date_of_birth",
    "gender",
    "familyID",
    "campID",
    "triage_category",
    "medical_conditions",
    "vital_status",
]
volunteers_fields = [
    "volunteerID",
    "first_name",
    "last_name",
    "username",
    "password",
    "date_of_birth",
    "phone",
    "account_status",
    "campID",
]


def clear_dummy_data():
    for table_name in ["plans", "camps", "volunteers", "refugees", "countries"]:
        q = f"""DELETE FROM {table_name}"""
        cursor.execute(q)
    conn.commit()


def insert_dummy_data():
    plans_data = """
    INSERT INTO plans (planID, start_date, end_date, name, country, event_name, description, shelter, water, food, medical_supplies, status, created_time) VALUES
    (1, '2023-01-01', '2025-01-01', 'London refugee camps', 'United Kingdom', 'UK Civil War', 'Refugees fleeing UK civil war', 200, 200, 200, 200, 'Active', '2023-01-01T14:36:25'),
    (2, '2023-01-01', '2025-01-01', 'French refugee camps', 'France', 'France Nuclear Disaster', 'Refugees fleeing Belleville nuclear meltdown', 300, 300, 300, 300, 'Active', '2023-01-01T14:36:25'),
    (3, '2023-01-01', '2025-01-01', 'Spanish refugee camps', 'Spain', 'Spanish Coup', 'Refugees fleeing Madrid coup', 300, 300, 300, 300, 'Active', '2023-01-01T14:36:25');
    """

    cursor.execute(plans_data)

    camp_data = """
    INSERT INTO camps (campID, location, shelter, water, food, medical_supplies, planID, created_time) VALUES
    (1, 'Camden', 20, 300, 600, 200, 1, '2023-01-01T14:36:25'),
    (2, 'Greenwich', 20, 300, 600, 200, 1, '2023-01-01T14:36:25'),
    (3, 'Paris', 20, 300, 600, 200, 2, '2023-01-01T14:36:25'),
    (4, 'Normandy', 20, 300, 600, 200, 2, '2023-01-01T14:36:25'),
    (5, 'Versailles', 20, 300, 600, 200, 2, '2023-01-01T14:36:25'),
    (6, 'Barcelona', 20, 300, 600, 200, 3,'2023-01-01T14:36:25'),
    (7, 'Valencia', 20, 300, 600, 200, 3,'2023-01-01T14:36:25');
    """

    cursor.execute(camp_data)

    # Insert dummy data for volunteers
    volunteers_data = """
    INSERT INTO volunteers (first_name, last_name, username, password, date_of_birth, phone, account_status, campID, created_time) VALUES
    -- Camp 1
    ('admin', 'admin', 'admin', '111', '1990-05-15', '555-1234', 'Active', NULL, '2023-01-01T14:36:25'),
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
    
    --Camp 4
    ('Ella', 'Bryant', 'volunteer25', '111', '1997-06-18', '555-2345', 'Active', 4, '2023-01-01T14:36:25'),
    ('Logan', 'Coleman', 'volunteer26', '111', '1989-01-12', '555-6789', 'Inactive', 4, '2023-01-01T14:36:25'),
    ('Avery', 'Reyes', 'volunteer27', '111', '1996-03-25', '555-8765', 'Active', 4, '2023-01-01T14:36:25'),
    
    --Camp 5
    ('Lucas', 'Scott', 'volunteer28', '111', '1992-07-08', '555-2345', 'Active', 5, '2023-01-01T14:36:25'),
    ('Sophie', 'Jordan', 'volunteer29', '111', '1995-09-20', '555-6789', 'Active', 5, '2023-01-01T14:36:25'),
    
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
    ('Isabella', 'Smith', '2002-08-10', 'Female', 1, 1, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Smith', '1980-03-25', 'Male', 1, 1, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Charlotte', 'Smith', '1995-12-05', 'Female', 1, 1, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Henry', 'Smith', '2010-05-18', 'Male', 1, 1, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophia', 'Williams', '1998-10-30', 'Female', 2, 1, 'Urgent', 'Respiratory Infection', 'Alive', '2023-01-01T14:36:25'),
    ('Jacob', 'Williams', '2014-06-22', 'Male', 2, 1, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Amelia', 'Williams', '2003-04-03', 'Female', 2, 1, 'Non-Urgent', 'Allergies', 'Alive', '2023-01-01T14:36:25'),
    ('William', 'Lee', '1990-01-12', 'Male', 3, 1, 'None', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    ('Sophie', 'Lee', '2005-09-20', 'Female', 3, 1, 'Non-Urgent', 'Heart Disease', 'Alive', '2023-01-01T14:36:25'),
    ('Thomas', 'Lee', '1988-07-08', 'Male', 3, 1, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Aisha', 'Lee', '1996-06-18', 'Female', 3, 1, 'Non-Urgent', 'Hypertension', 'Alive', '2023-01-01T14:36:25'),
    ('Alexander', 'Lee', '1983-08-14', 'Male', 3, 1, 'None', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Lily', 'Patel', '2007-11-02', 'Female', 4, 1, 'None', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Anand', 'Patel', '2000-02-25', 'Male', 4, 1, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Meena', 'Patel', '1993-03-12', 'Female', 4, 1, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Leo', 'Jones', '2012-12-30', 'Male', 5, 1, 'None', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Zara', 'Jones', '2005-07-28', 'Female', 5, 1, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'Evans', '1998-04-15', 'Female', 6, 1, 'None', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Nooh', 'Evans', '2011-09-10', 'Male', 6, 1, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Liam', 'Thompson', '2004-05-05', 'Male', 7, 1, 'None', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),

    -- Camp 2
    ('Emily', 'White', '2001-11-10', 'Female', 8, 2, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Alexander', 'White', '1995-03-25', 'Male', 8, 2, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'White', '2008-12-05', 'Female', 8, 2, 'None', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Leo', 'White', '2012-05-18', 'Male', 8, 2, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Isabella', 'White', '1999-09-30', 'Female', 8, 2, 'Urgent', 'Respiratory Infection', 'Alive', '2023-01-01T14:36:25'),
    ('James', 'Martin', '2007-11-15', 'Male', 9, 2, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Poppy', 'Martin', '2015-04-03', 'Female', 9, 2, 'None', 'Allergies', 'Alive', '2023-01-01T14:36:25'),
    ('Jack', 'Martin', '1988-06-22', 'Male', 9, 2, 'None', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    ('Ruby', 'Martin', '2003-09-20', 'Female', 9, 2, 'Urgent', 'Heart Disease', 'Alive', '2023-01-01T14:36:25'),
    ('George', 'Jones', '1994-07-08', 'Male', 5, 2, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophie', 'Jones', '1996-06-18', 'Female', 5, 2, 'Urgent', 'Hypertension', 'Alive', '2023-01-01T14:36:25'),
    ('Benjamin', 'Hill', '1983-08-14', 'Male', 10, 2, 'Immediate', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Isla', 'Hill', '2007-11-02', 'Female', 10, 2, 'None', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Jacob', 'Hill', '2000-02-25', 'Male', 10, 2, 'Immediate', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ella', 'Hill', '1993-03-12', 'Female', 10, 2, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Thompson', '2012-12-30', 'Male', 7, 2, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Zara', 'Thompson', '2005-07-28', 'Female', 7, 2, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ava', 'Thompson', '1998-04-15', 'Female', 7, 2, 'Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Noah', 'Lee', '2011-09-10', 'Male', 3, 2, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ethan', 'Lee', '2004-05-05', 'Male', 3, 2, 'Immediate', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),

    -- Camp 3
    ('Lily', 'Harrison', '1996-04-20', 'Female', 11, 3, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Harrison', '2002-08-15', 'Male', 11, 3, 'Urgent', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Ava', 'Harrison', '2010-10-05', 'Female', 11, 3, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Ethan', 'Clark', '2014-11-18', 'Male', 12, 3, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'Clark', '2001-09-30', 'Female', 12, 3, 'Urgent', 'Respiratory Infection', 'Alive', '2023-01-01T14:36:25'),
    ('Noah', 'Clark', '2012-01-15', 'Male', 12, 3, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Layla', 'Thompson', '2015-04-02', 'Female', 7, 3, 'Non-Urgent', 'Allergies', 'Alive', '2023-01-01T14:36:25'),
    ('Oliver', 'Robert', '1998-01-12', 'Male', 13, 3, 'None', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    
    -- Camp 4
    ('Isla', 'Dupont', '2005-09-20', 'Female', 14, 4, 'Urgent', 'Heart Disease', 'Alive', '2023-01-01T14:36:25'),
    ('Louis', 'Dupont', '1992-07-08', 'Male', 14, 4, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophia', 'Dupont', '1996-06-18', 'Female', 14, 4, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Paulo', 'Vidal', '1983-08-14', 'Male', 15, 4, 'Immediate', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Eva', 'Vidal', '2007-11-02', 'Female', 15, 4, 'Non-Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Daniel', 'Vidal', '2000-02-25', 'Male', 15, 4, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Sophie', 'Nguyen', '1993-03-12', 'Female', 16, 4, 'Standard', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Leo', 'Nguyen', '2012-12-30', 'Male', 16, 4, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Zara', 'Nguyen', '2005-07-28', 'Female', 16, 4, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Mia', 'Nguyen', '1998-04-15', 'Female', 16, 4, 'Urgent', 'Asthma', 'Alive', '2023-01-01T14:36:25'),
    ('Noah', 'Robert', '2011-09-10', 'Male', 13, 4, 'Non-Urgent', 'None', 'Alive', '2023-01-01T14:36:25'),
    ('Ella', 'Robert', '2004-05-05', 'Male', 13, 4, 'None', 'Fractured Arm', 'Alive', '2023-01-01T14:36:25'),
    
    -- Camp 5
    ('Camilla', 'Diaz', '1998-02-19', 'Female', 17, 5, 'Immediate', 'Fractured Leg', 'Alive', '2023-01-01T14:36:25'),
    ('Antonio', 'Garcia', '1983-08-14', 'Male', 18, 5, 'None', 'None', 'Alive', '2023-01-01T14:36:25'),
    
    -- Camp 6
    ('Rafael', 'Diaz', '1980-08-19', 'Male', 17, 6, 'None', 'Diabetes', 'Alive', '2023-01-01T14:36:25'),
    ('Victoria', 'Garcia', '1970-09-23', 'Female', 18, 6, 'None', 'None', 'Alive', '2023-01-01T14:36:25')
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

    # cursor.execute("""
    # INSERT INTO current_user (id, username) VALUES (1, 'default_user')
    # ON CONFLICT(id) DO UPDATE SET username = 'default_user';
    # """)

    conn.commit()


def check_sample_db_init():
    cursor.execute(
        "SELECT * FROM volunteers WHERE username = 'admin' and password = '111'"
    )
    return cursor.fetchone() is None


create_database()

triggers_for_audit_table("plans", plans_fields, "planID")
triggers_for_audit_table("camps", camps_fields, "campID")
triggers_for_audit_table("refugees", refugees_fields, "refugeeID")
triggers_for_audit_table("volunteers", volunteers_fields, "volunteerID")

if __name__ == "__main__" or check_sample_db_init():
    print("Inserting dummy data...")
    clear_dummy_data()
    insert_dummy_data()
