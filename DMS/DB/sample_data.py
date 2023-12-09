from config import conn, cursor

def clear_dummy_data():
    for table_name in ["plans", "camps", "volunteers", "refugees", "countries"]:
        q = f"""DELETE FROM {table_name}"""
        cursor.execute(q)
    conn.commit()

def insert_dummy_data():
    plans_data = """
    INSERT INTO plans (planID, start_date, end_date, name, country, event_name, description) VALUES
    (1, '2023-01-01', '2025-01-01', 'Wylfa Nuclear Meltdown', 'United Kingdom', 'Nuclear Crisis Management', 'Emergency response to nuclear meltdown on Anglesey'),
    (2, '2023-01-01', '2025-01-01', 'London Virus Outbreak', 'United Kingdom', 'Virus Containment Effort', 'Response to widespread virus outbreak in London'),
    (3, '2023-01-01', '2025-01-01', 'Paris Earthquake Response', 'France', 'Earthquake Relief', 'Relief efforts for earthquake in Paris');
    """

    cursor.execute(plans_data)

    camp_data = """
    INSERT INTO camps (campID, location, max_shelter, water, max_water, food, max_food, medical_supplies, max_medical_supplies, planID) VALUES
    (1, 'Camden', 71, 409, 562, 478, 593, 164, 214, 1),
    (2, 'Greenwich', 198, 103, 190, 335, 502, 57, 119, 1),
    (3, 'Snowdonia', 179, 334, 545, 310, 531, 160, 248, 2),
    (4, 'Richmond', 135, 470, 741, 175, 360, 98, 181, 2),
    (5, 'Versailles', 164, 260, 537, 394, 637, 88, 222, 3)
    """

    cursor.execute(camp_data)

 # Insert dummy data for volunteers
    volunteers_data = """
    INSERT INTO volunteers (first_name, last_name, username, password, date_of_birth, phone, account_status, campID) VALUES
    -- Camp 1
    ('admin', '111', 'admin', '111', '1990-05-15', '555-1234', 'Active', NULL),
    ('Jane', 'Smith', 'volunteer1', '111', '1985-08-22', '555-5678', 'Active', 1),
    ('Robert', 'Johnson', 'robert_j', 'password789', '1992-03-10', '555-9876', 'Active', 1),
    ('Emily', 'Williams', 'emily_w', 'passwordabc', '1988-11-27', '555-4321', 'Active', 1),
    ('Michael', 'Brown', 'michael_b', 'passworddef', '1995-07-18', '555-8765', 'Inactive', 1),
    ('Sophia', 'Davis', 'sophia_d', 'pass123', '1993-09-05', '555-2345', 'Active', 1),
    ('David', 'Anderson', 'david_a', 'pass456', '1991-02-14', '555-6789', 'Inactive', 1),
    ('Olivia', 'Thomas', 'olivia_t', 'pass789', '1986-12-03', '555-8765', 'Active', 1),
    ('Christopher', 'Garcia', 'chris_g', 'passabc', '1994-04-20', '555-2345', 'Active', 1),
    ('Emma', 'Johnson', 'emma_j', 'pass789', '1998-06-08', '555-5678', 'Active', 1),

    -- Camp 2
    ('Daniel', 'White', 'volunteer2', '222', '1987-10-12', '555-3456', 'Active', 2),
    ('Sophie', 'Miller', 'sophie_m', 'pass456', '1994-01-25', '555-7890', 'Active', 2),
    ('Matthew', 'Davis', 'matthew_d', 'pass789', '1990-09-30', '555-2345', 'Active', 2),
    ('Ava', 'Wilson', 'ava_w', 'passabc', '1985-12-15', '555-6789', 'Active', 2),
    ('Nicholas', 'Taylor', 'nicholas_t', 'passdef', '1992-05-18', '555-8765', 'Inactive', 2),
    ('Grace', 'Moore', 'grace_m', 'passghi', '1997-03-22', '555-1234', 'Active', 2),
    ('Ethan', 'Baker', 'ethan_b', 'passjkl', '1988-08-08', '555-5678', 'Inactive', 2),
    ('Chloe', 'Fisher', 'chloe_f', 'passmno', '1995-04-02', '555-2345', 'Active', 2),
    ('Caleb', 'Ward', 'caleb_w', 'passpqr', '1989-11-10', '555-6789', 'Active', 2),
    ('Madison', 'Perry', 'madison_p', 'passtu', '1996-07-17', '555-8765', 'Active', 2),

    -- Camp 3
    ('Liam', 'Carter', 'volunteer3', '333', '1993-02-05', '555-2345', 'Active', 3),
    ('Aubrey', 'Hayes', 'aubrey_h', 'passyz1', '1998-08-20', '555-6789', 'Active', 3),
    ('Mason', 'Wells', 'mason_w', 'pass234', '1991-04-15', '555-1234', 'Active', 3),
    ('Harper', 'Barnes', 'harper_b', 'pass567', '1986-10-30', '555-5678', 'Active', 3),
    ('Aiden', 'Fisher', 'aiden_f', 'pass890', '1994-12-22', '555-8765', 'Inactive', 3),
    ('Ella', 'Bryant', 'ella_b', 'passabc1', '1997-06-18', '555-2345', 'Active', 3),
    ('Logan', 'Coleman', 'logan_c', 'passdef1', '1989-01-12', '555-6789', 'Inactive', 3),
    ('Avery', 'Reyes', 'avery_r', 'passghi1', '1996-03-25', '555-8765', 'Active', 3),
    ('Lucas', 'Scott', 'lucas_s', 'passjkl1', '1992-07-08', '555-2345', 'Active', 3),
    ('Sophie', 'Jordan', 'sophie_j', 'passmno1', '1995-09-20', '555-6789', 'Active', 3)
    """

    cursor.execute(volunteers_data)

    refugees_data = """
    INSERT INTO refugees (first_name, last_name, date_of_birth, gender, familyID, campID, triage_category, medical_conditions, vital_status) VALUES

    --Family separated: 8, 10, 

    -- Camp 1
    ('Isabella', 'Johnson', '2002-08-10', 'Female', 1, 1, 'Standard', 'None', 'Alive'),
    ('Oliver', 'Smith', '1980-03-25', 'Male', 2, 1, 'Urgent', 'Diabetes', 'Alive'),
    ('Charlotte', 'Taylor', '1995-12-05', 'Female', 3, 1, 'Non-Urgent', 'Asthma', 'Alive'),
    ('Henry', 'Clark', '2010-05-18', 'Male', 4, 1, 'None', 'None', 'Alive'),
    ('Sophia', 'Williams', '1998-10-30', 'Female', 5, 1, 'Urgent', 'Respiratory Infection', 'Alive'),
    ('Jacob', 'Brown', '2014-06-22', 'Male', 6, 1, 'Standard', 'None', 'Alive'),
    ('Amelia', 'Harrison', '2003-04-03', 'Female', 7, 1, 'Non-Urgent', 'Allergies', 'Alive'),
    ('William', 'Baker', '1990-01-12', 'Male', 8, 1, 'None', 'Fractured Arm', 'Alive'),
    ('Sophie', 'Evans', '2005-09-20', 'Female', 9, 1, 'Urgent', 'Heart Disease', 'Alive'),
    ('Thomas', 'Jones', '1988-07-08', 'Male', 10, 1, 'Non-Urgent', 'None', 'Alive'),
    ('Aisha', 'Khan', '1996-06-18', 'Female', 11, 1, 'Urgent', 'Hypertension', 'Alive'),
    ('Alexander', 'Brown', '1983-08-14', 'Male', 12, 1, 'None', 'Fractured Leg', 'Alive'),
    ('Lily', 'Taylor', '2007-11-02', 'Female', 13, 1, 'Non-Urgent', 'Asthma', 'Alive'),
    ('Daniel', 'Evans', '2000-02-25', 'Male', 9, 1, 'None', 'None', 'Alive'),
    ('Ella', 'Williams', '1993-03-12', 'Female', 15, 1, 'Standard', 'None', 'Alive'),
    ('Leo', 'Jones', '2012-12-30', 'Male', 10, 1, 'Urgent', 'Diabetes', 'Alive'),
    ('Zara', 'Clark', '2005-07-28', 'Female', 17, 1, 'Non-Urgent', 'None', 'Alive'),
    ('Mia', 'Evans', '1998-04-15', 'Female', 9, 1, 'Urgent', 'Asthma', 'Alive'),
    ('Nooh', 'Baker', '2011-09-10', 'Male', 8, 1, 'Non-Urgent', 'None', 'Alive'),
    ('Liam', 'Thompson', '2004-05-05', 'Male', 20, 1, 'None', 'Fractured Arm', 'Alive'),

    -- Camp 2
    ('Emily', 'White', '2001-11-10', 'Female', 21, 2, 'Standard', 'None', 'Alive'),
    ('Alexander', 'Miller', '1995-03-25', 'Male', 22, 2, 'Urgent', 'Diabetes', 'Alive'),
    ('Mia', 'Davis', '2008-12-05', 'Female', 23, 2, 'Non-Urgent', 'Asthma', 'Alive'),
    ('Leo', 'Baker', '2012-05-18', 'Male', 8, 2, 'Immediate', 'None', 'Alive'),
    ('Isabella', 'Clark', '1999-09-30', 'Female', 25, 2, 'Urgent', 'Respiratory Infection', 'Alive'),
    ('James', 'Martin', '2007-11-15', 'Male', 26, 2, 'Standard', 'None', 'Alive'),
    ('Poppy', 'Harrison', '2015-04-03', 'Female', 7, 2, 'Non-Urgent', 'Allergies', 'Alive'),
    ('Jack', 'Baker', '1988-06-22', 'Male', 8, 2, 'Immediate', 'Fractured Arm', 'Alive'),
    ('Ruby', 'Evans', '2003-09-20', 'Female', 29, 2, 'Urgent', 'Heart Disease', 'Alive'),
    ('George', 'Jones', '1994-07-08', 'Male', 10, 2, 'Non-Urgent', 'None', 'Alive'),
    ('Sophie', 'Harrison', '1996-06-18', 'Female', 7, 2, 'Urgent', 'Hypertension', 'Alive'),
    ('Benjamin', 'Hill', '1983-08-14', 'Male', 32, 2, 'Immediate', 'Fractured Leg', 'Alive'),
    ('Isla', 'Clark', '2007-11-02', 'Female', 33, 2, 'Non-Urgent', 'Asthma', 'Alive'),
    ('Jacob', 'Evans', '2000-02-25', 'Male', 29, 2, 'Immediate', 'None', 'Alive'),
    ('Ella', 'Williams', '1993-03-12', 'Female', 35, 2, 'Standard', 'None', 'Alive'),
    ('Oliver', 'Jones', '2012-12-30', 'Male', 10, 2, 'Urgent', 'Diabetes', 'Alive'),
    ('Zara', 'Clark', '2005-07-28', 'Female', 37, 2, 'Non-Urgent', 'None', 'Alive'),
    ('Ava', 'Evans', '1998-04-15', 'Female', 29, 2, 'Urgent', 'Asthma', 'Alive'),
    ('Noah', 'Baker', '2011-09-10', 'Male', 39, 2, 'Non-Urgent', 'None', 'Alive'),
    ('Ethan', 'Thompson', '2004-05-05', 'Male', 40, 2, 'Immediate', 'Fractured Arm', 'Alive'),

    -- Camp 3
    ('Lily', 'White', '1996-04-20', 'Female', 41, 3, 'Standard', 'None', 'Alive'),
    ('Oliver', 'Taylor', '2002-08-15', 'Male', 42, 3, 'Urgent', 'Diabetes', 'Alive'),
    ('Ava', 'Harrison', '2010-10-05', 'Female', 7, 3, 'Non-Urgent', 'Asthma', 'Alive'),
    ('Ethan', 'Baker', '2014-11-18', 'Male', 39, 3, 'Immediate', 'None', 'Alive'),
    ('Mia', 'Williams', '2001-09-30', 'Female', 45, 3, 'Urgent', 'Respiratory Infection', 'Alive'),
    ('Noah', 'Martin', '2012-01-15', 'Male', 46, 3, 'Standard', 'None', 'Alive'),
    ('Layla', 'Harrison', '2015-04-02', 'Female', 7, 3, 'Non-Urgent', 'Allergies', 'Alive'),
    ('Oliver', 'Baker', '1998-01-12', 'Male', 39, 3, 'Immediate', 'Fractured Arm', 'Alive'),
    ('Isla', 'Evans', '2005-09-20', 'Female', 49, 3, 'Urgent', 'Heart Disease', 'Alive'),
    ('Harry', 'Jones', '1992-07-08', 'Male', 10, 3, 'Non-Urgent', 'None', 'Alive'),
    ('Sophia', 'Taylor', '1996-06-18', 'Female', 51, 3, 'Urgent', 'Hypertension', 'Alive'),
    ('Henry', 'Hill', '1983-08-14', 'Male', 52, 3, 'Immediate', 'Fractured Leg', 'Alive'),
    ('Eva', 'Clark', '2007-11-02', 'Female', 53, 3, 'Non-Urgent', 'Asthma', 'Alive'),
    ('Daniel', 'Evans', '2000-02-25', 'Male', 49, 3, 'Immediate', 'None', 'Alive'),
    ('Sophie', 'Williams', '1993-03-12', 'Female', 55, 3, 'Standard', 'None', 'Alive'),
    ('Leo', 'Jones', '2012-12-30', 'Male', 10, 3, 'Urgent', 'Diabetes', 'Alive'),
    ('Zara', 'Clark', '2005-07-28', 'Female', 57, 3, 'Non-Urgent', 'None', 'Alive'),
    ('Mia', 'Evans', '1998-04-15', 'Female', 49, 3, 'Urgent', 'Asthma', 'Alive'),
    ('Noah', 'Baker', '2011-09-10', 'Male', 8, 3, 'Non-Urgent', 'None', 'Alive'),
    ('Ella', 'Thompson', '2004-05-05', 'Male', 60, 3, 'Immediate', 'Fractured Arm', 'Alive')
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

    conn.commit()

clear_dummy_data()
insert_dummy_data()

conn.close()
