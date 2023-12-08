from .config import conn, cursor


def insert_dummy_data():
    plans_data = """
    INSERT INTO plans (planID, start_date, end_date, name, country, event_name, description) VALUES
    (1, '01/01/2023', '31/12/2024', 'Wylfa Nuclear Meltdown', 'United Kingdom', 'Nuclear Crisis Management', 'Emergency response to nuclear meltdown on Anglesey'),
    (2, '01/01/2023', '31/12/2024', 'London Virus Outbreak', 'United Kingdom', 'Virus Containment Effort', 'Response to widespread virus outbreak in London'),
    (3, '01/01/2023', '31/12/2024', 'Paris Earthquake Response', 'France', 'Earthquake Relief', 'Relief efforts for earthquake in Paris');
    """

    cursor.execute(plans_data)

    camp_data = """
    INSERT INTO camps (campID, location, max_shelter, water, max_water, food, max_food, medical_supplies, max_medical_supplies, planID) VALUES
    (1, 'Camden', 71, 409, 562, 478, 593, 164, 214, 2),
    (2, 'Greenwich', 198, 103, 190, 335, 502, 57, 119, 2),
    (3, 'Snowdonia', 179, 334, 545, 310, 531, 160, 248, 1),
    (4, 'Richmond', 135, 470, 741, 175, 360, 98, 181, 2),
    (5, 'Versailles', 164, 260, 537, 394, 637, 88, 222, 3),
    (6, 'Montmartre', 171, 238, 372, 197, 284, 156, 217, 3),
    (7, 'Anglesey', 182, 380, 451, 449, 746, 136, 230, 1),
    (8, 'Aberdaron', 54, 267, 407, 449, 539, 138, 198, 1),
    (9, 'Marais', 168, 481, 687, 177, 392, 155, 303, 3),
    (10, 'Llandudno', 124, 414, 661, 263, 458, 105, 213, 1),
    (11, 'Wimbledon', 190, 153, 294, 403, 513, 158, 217, 2),
    (12, 'Brixton', 177, 169, 463, 431, 578, 165, 250, 2),
    (13, 'Belleville', 160, 497, 569, 428, 575, 172, 279, 3),
    (14, 'Montparnasse', 193, 383, 576, 361, 590, 175, 225, 3),
    (15, 'Conwy', 139, 300, 548, 425, 694, 87, 167, 1),
    (16, 'Saint-Germain', 130, 347, 435, 259, 344, 67, 206, 3),
    (17, 'Bastille', 78, 153, 368, 458, 722, 60, 187, 3),
    (18, 'La Chapelle', 88, 174, 434, 200, 435, 162, 240, 3),
    (19, 'Oberkampf', 98, 461, 603, 184, 274, 170, 252, 3),
    (20, 'Shoreditch', 63, 360, 552, 415, 653, 166, 250, 2);
    """

    cursor.execute(camp_data)

    volunteer_data = """
    INSERT INTO volunteers VALUES
    (1, 'Michael', 'Williams', 'Volunteer1', '111', '25/03/1986', '555-812-5460', 'Active', 11),
    (2, 'Tim', 'Garcia', 'Volunteer2', '111', '07/04/1998', '555-416-1396', 'Active', 5),
    (3, 'Mary', 'Williams', 'Volunteer3', '111', '10/04/1993', '555-718-5482', 'Active', 1),
    (4, 'James', 'Garcia', 'Volunteer4', '111', '13/01/1998', '555-261-8163', 'Active', 1),
    (5, 'Malcolm', 'Johnson', 'Volunteer5', '111', '07/02/1992', '555-990-5311', 'Active', 7),
    (6, 'Patricia', 'Martinez', 'Volunteer6', '111', '24/12/2000', '555-125-5228', 'Active', 10),
    (7, 'Mary', 'Martinez', 'Volunteer7', '111', '19/03/1971', '555-785-8777', 'Active', 7),
    (8, 'Nikolaas', 'Youcef', 'Volunteer8', '111', '08/10/1971', '555-315-3013', 'Active', 3),
    (9, 'Declan', 'Johnson', 'Volunteer9', '111', '23/09/1977', '555-900-8343', 'Active', 10),
    (10, 'Jennifer', 'Miller', 'Volunteer10', '111', '01/01/1986', '555-949-5827', 'Active', 10),
    (11, 'James', 'Rodriguez', 'Volunteer11', '111', '12/01/1997', '555-978-1129', 'Active', 7),
    (12, 'Baz', 'Smith', 'Volunteer12', '111', '28/05/1993', '555-747-1912', 'Active', 1),
    (13, 'Jennifer', 'Brown', 'Volunteer13', '111', '09/10/1988', '555-986-5681', 'Inactive', 2),
    (14, 'Michael', 'Jones', 'Volunteer14', '111', '08/09/1988', '555-567-1308', 'Active', 1),
    (15, 'Francis', 'Miller', 'Volunteer15', '111', '28/03/1983', '555-923-9116', 'Inactive', 8),
    (16, 'Rafiq', 'Andreas', 'Volunteer16', '111', '02/10/1975', '555-155-3398', 'Active', 4),
    (17, 'James', 'Jones', 'Volunteer17', '111', '09/10/1978', '555-345-1083', 'Inactive', 4),
    (18, 'Robert', 'Brown', 'Volunteer18', '111', '01/02/1984', '555-409-9962', 'Inactive', 6),
    (19, 'Kiran', 'Smith', 'Volunteer19', '111', '26/11/1983', '555-164-8972', 'Inactive', 4),
    (20, 'Michael', 'Rodriguez', 'Volunteer20', '111', '17/02/1973', '555-346-3098', 'Active', 5),
    (21, 'Robert', 'Davis', 'Volunteer21', '111', '02/05/1989', '555-570-6934', 'Active', 8),
    (22, 'Ira', 'Erika', 'Volunteer22', '111', '28/12/1977', '555-198-7654', 'Inactive', 2),
    (23, 'Emma', 'Jones', 'Volunteer23', '111', '15/07/1999', '555-222-1234', 'Active', 3),
    (24, 'Daniil', 'Lileas', 'Volunteer24', '111', '19/08/1985', '555-234-5678', 'Inactive', 4),
    (25, 'Marco', 'Smith', 'Volunteer25', '111', '30/11/1976', '555-345-6789', 'Active', 5),
    (26, 'Patricia', 'Johnson', 'Volunteer26', '111', '21/06/1987', '555-456-7890', 'Inactive', 6),
    (27, 'Sevda', 'Oto', 'Volunteer27', '111', '10/04/1978', '555-567-8901', 'Active', 7),
    (28, 'Michael', 'Garcia', 'Volunteer28', '111', '17/09/1982', '555-678-9012', 'Inactive', 8),
    (29, 'Linda', 'Miller', 'Volunteer29', '111', '06/12/1979', '555-789-0123', 'Active', 9),
    (30, 'Ana', 'Cezara', 'Volunteer30', '111', '22/03/1990', '555-890-1234', 'Inactive', 10);
    """

    cursor.execute(volunteer_data)

    refugee_data = """
    INSERT INTO refugees (refugeeID, first_name, last_name, date_of_birth, gender, familyID, campID, triage_category,
    medical_conditions, vital_status) VALUES
    (1, 'Aisha', 'Kumar', '08/12/1946', 'Female', 645, 4, 'Standard', 'Asthma Diabetes','Deceased'),
    (2, 'Liam', 'Nguyen', '16/06/1998', 'Male', 239, 15, 'None', NULL,'Alive'),
    (3, 'Fatima', 'Chen', '05/09/1939', 'Female', 139, 5, 'None', NULL,'Deceased'),
    (4, 'Gail', 'Khan', '02/06/2006', 'Female', 909, 15, 'Non-Urgent', 'Ehlers-danlos syndrome Postural orthostatic tachycardia syndrome','Alive'),
    (5, 'Carlos', 'Garcia', '28/08/1992', 'Male', 834, 11, 'None', NULL, 'Alive'),
    (6, 'Sara', 'Ali', '10/11/2009', 'Female', 633, 16, 'None', NULL,'Alive'),
    (7, 'George', 'Kim', '01/12/1930', 'Male', 171, 11, 'None', NULL,'Alive'),
    (8, 'Amina', 'Hassan', '08/07/1990', 'Female', 572, 8, 'Immediate', 'Stroke','Alive'),
    (9, 'Ivan', 'Petrov', '07/06/1939', 'Male', 428, 1, 'None', NULL,'Deceased'),
    (10, 'Yuki', 'Tanaka', '02/11/1964', 'Female', 49, 14, 'Standard', NULL,'Alive'),
    (11, 'Mohamed', 'Al-Sayed', '31/03/1987', 'Male', 119, 4, 'None', NULL,'Alive'),
    (12, 'Allan', 'Johnson', '27/12/1968', 'Male', 840, 15, 'None', NULL,'Deceased'),
    (13, 'Yulia', 'Ivanova', '19/02/1941', 'Female', 305, 5, 'None', NULL,'Alive'),
    (14, 'Lerato', 'Nkosi', '03/01/1978', 'Female', 463, 10, 'Urgent', 'Brain Tumour','Alive'),
    (15, 'Jin', 'Lee', '06/09/2022', 'Male', 19, 10, 'None', NULL,'Alive'),
    (16, 'Shannon', 'OConnor', '23/10/1947', 'Female', 6, 5, 'Very-Urgent', 'Coronary heart disease', 'Alive'),
    (17, 'Keisha', 'Williams', '21/10/1944', 'Female', 597, 3, 'None', NULL,'Alive'),
    (18, 'Maria', 'Fernandez', '09/09/2005', 'Female', 516, 9, 'Immediate', 'Heart Failure','Alive'),
    (19, 'Kim', 'Park', '16/10/2015', 'Male', 725, 12, 'Very-Urgent', 'Chronic Obstructive Pulmonary Disease (COPD)','Alive'),
    (20, 'Melissa', 'Smith', '22/08/1956', 'Female', 71, 10, 'None', NULL,'Deceased'),
    (21, 'Stephanie', 'Martinez', '24/03/2023', 'Female', 788, 1, 'None', NULL,'Deceased'),
    (22, 'Gavin', 'OReilly', '06/04/1950', 'Male', 622, 6, 'Very-Urgent', 'Chronic Obstructive Pulmonary Disease (COPD)','Alive'),
    (23, 'Olivia', 'Brown', '26/03/2021', 'Female', 462, 8, 'None', NULL,'Alive'),
    (24, 'Elliot', 'Moreau', '14/08/1934', 'Male', 747, 17, 'None', NULL,'Alive'),
    (25, 'Rosemary', 'Johnson', '07/12/2020', 'Female', 971, 19, 'Very-Urgent', 'Chronic Obstructive Pulmonary Disease (COPD)','Alive'),
    (26, 'Kevin', 'Wong', '15/04/1993', 'Male', 678, 10, 'None', NULL,'Deceased'),
    (27, 'Ananya', 'Patel', '05/11/1995', 'Female', 246, 20, 'Standard', 'Coronary heart disease','Alive'),
    (28, 'Alexandra', 'Silva', '25/07/1979', 'Female', 176, 6, 'None', NULL,'Alive'),
    (29, 'Dylan', 'Murphy', '18/09/2021', 'Male', 783, 19, 'Urgent', 'Pneunia','Alive'),
    (30, 'Frank', 'Schneider', '13/08/1981', 'Male', 862, 2, 'None', NULL,'Alive'),
    (31, 'Ben', 'Singh', '05/07/2020', 'Male', 916, 13, 'None', NULL,'Alive'),
    (32, 'Melanie', 'Bennett', '21/12/1938', 'Female', 140, 4, 'Standard', 'Crohns Disease','Alive'),
    (33, 'Hollie', 'Anderson', '17/03/1937', 'Female', 918, 5, 'Urgent', 'HIV','Alive'),
    (34, 'Jonathan', 'Carroll', '11/11/1982', 'Male', 830, 8, 'Non-Urgent', 'Anemia','Alive'),
    (35, 'Dawn', 'Harvey', '06/08/1959', 'Female', 182, 17, 'None', NULL,'Alive'),
    (36, 'Shane', 'Lamb', '03/10/1962', 'Male', 228, 4, 'None', NULL,'Alive'),
    (37, 'Callum', 'Smith', '27/07/1939', 'Male', 931, 14, 'Urgent', 'Asthma','Alive'),
    (38, 'Jade', 'Higgins', '15/09/1980', 'Female', 400, 7, 'None', NULL,'Alive'),
    (39, 'Hazel', 'Cole', '08/09/1957', 'Female', 190, 16, 'None', NULL,'Alive'),
    (40, 'Max', 'Stevens', '18/07/2018', 'Male', 40, 19, 'None', NULL,'Alive'),
    (41, 'Raymond', 'Middleton', '21/07/2021', 'Male', 253, 19, 'Non-Urgent', 'Kidney Stones','Alive'),
    (42, 'Peter', 'Douglas', '20/08/1997', 'Male', 836, 17, 'None', NULL,'Alive'),
    (43, 'Richard', 'Butcher', '10/01/1986', 'Male', 684, 8, 'Non-Urgent', 'Rheumatoid Arthritis','Alive'),
    (44, 'Ross', 'Turner', '31/07/2005', 'Male', 616, 3, 'None', NULL,'Alive'),
    (45, 'Hollie', 'Fraser', '19/09/1994', 'Female', 652, 10, 'None', NULL,'Alive');
    """

    cursor.execute(refugee_data)

    set_volunteer_usernames_passwords = """
    WITH RankedVolunteers AS (
        SELECT
            volunteerID,
            ROW_NUMBER() OVER (ORDER BY volunteerID) AS rn
        FROM
            volunteers
        )
        UPDATE volunteers
        SET
            password = '111',
            username = 'volunteer' ||
                (SELECT rn FROM RankedVolunteers 
                WHERE volunteers.volunteerID = RankedVolunteers.volunteerID);
        """

    cursor.execute(set_volunteer_usernames_passwords)

    insert_admin = """
    INSERT
    INTO
    volunteers
    VALUES
    (31, 'Michael', 'Williams', 'admin', '111', '25/03/1986', '555-812-5460', NULL, NULL)
    """

    cursor.execute(insert_admin)

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


insert_dummy_data()

conn.close()
