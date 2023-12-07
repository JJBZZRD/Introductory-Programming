from config import conn, cursor


def insert_dummy_data():
    plans_data = """
    INSERT INTO plans (planID, start_date, end_date, name, country, event_name, description) VALUES
    (1, '01/01/2023', '31/12/2024', 'Wylfa Nuclear Meltdown', 'Wylfa', 'Nuclear Crisis Management', 'Emergency response to nuclear meltdown'),
    (2, '01/01/2023', '31/12/2024', 'London Virus Outbreak', 'London', 'Virus Containment Effort', 'Response to widespread virus outbreak in London'),
    (3, '01/01/2023', '31/12/2024', 'Paris Earthquake Response', 'Paris', 'Earthquake Relief', 'Relief efforts for earthquake in Paris');
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
    (1, 'Michael', 'Williams', 'jjones1', 'pass', '25/03/1986', '555-812-5460', 'Active', 11),
    (2, 'Elizabeth', 'Garcia', 'lrodriguez2', 'pass', '07/04/1998', '555-416-1396', 'Active', 5),
    (3, 'Mary', 'Williams', 'rdavis3', 'pass', '10/04/1993', '555-718-5482', 'Active', 1),
    (4, 'James', 'Garcia', 'jbrown4', 'pass', '13/01/1998', '555-261-8163', 'Active', 1),
    (5, 'Patricia', 'Johnson', 'pjohnson5', 'pass', '07/02/1992', '555-990-5311', 'Active', 7),
    (6, 'Patricia', 'Martinez', 'ljones6', 'pass', '24/12/2000', '555-125-5228', 'Active', 10),
    (7, 'Mary', 'Martinez', 'jmiller7', 'pass', '19/03/1971', '555-785-8777', 'Active', 7),
    (8, 'John', 'Jones', 'lbrown8', 'pass', '08/10/1971', '555-315-3013', 'Active', 3),
    (9, 'Michael', 'Johnson', 'jgarcia9', 'pass', '23/09/1977', '555-900-8343', 'Active', 10),
    (10, 'Jennifer', 'Miller', 'prodriguez10', 'pass', '01/01/1986', '555-949-5827', 'Active', 10),
    (11, 'James', 'Rodriguez', 'wmartinez11', 'pass', '12/01/1997', '555-978-1129', 'Active', 7),
    (12, 'John', 'Smith', 'jsmith12', 'pass', '28/05/1993', '555-747-1912', 'Active', 1),
    (13, 'Jennifer', 'Brown', 'lwilliams13', 'pass', '09/10/1988', '555-986-5681', 'Inactive', 2),
    (14, 'Michael', 'Jones', 'jsmith14', 'pass', '08/09/1988', '555-567-1308', 'Active', 1),
    (15, 'James', 'Miller', 'wjones15', 'pass', '28/03/1983', '555-923-9116', 'Inactive', 8),
    (16, 'John', 'Williams', 'jrodriguez16', 'pass', '02/10/1975', '555-155-3398', 'Active', 4),
    (17, 'James', 'Jones', 'lrodriguez17', 'pass', '09/10/1978', '555-345-1083', 'Inactive', 4),
    (18, 'Robert', 'Brown', 'emiller18', 'pass', '01/02/1984', '555-409-9962', 'Inactive', 6),
    (19, 'Michael', 'Smith', 'rsmith19', 'pass', '26/11/1983', '555-164-8972', 'Inactive', 4),
    (20, 'Michael', 'Rodriguez', 'rsmith20', 'pass', '17/02/1973', '555-346-3098', 'Active', 5),
    (21, 'Robert', 'Davis', 'wgarcia21', 'pass', '02/05/1989', '555-570-6934', 'Active', 8),
    (22, 'William', 'Williams', 'jmartinez22', 'pass', '28/12/1977', '555-198-7654', 'Inactive', 2),
    (23, 'Jennifer', 'Jones', 'rjones23', 'pass', '15/07/1999', '555-222-1234', 'Active', 3),
    (24, 'John', 'Brown', 'jbrown24', 'pass', '19/08/1985', '555-234-5678', 'Inactive', 4),
    (25, 'James', 'Smith', 'jsmith25', 'pass', '30/11/1976', '555-345-6789', 'Active', 5),
    (26, 'Patricia', 'Johnson', 'pjohnson26', 'pass', '21/06/1987', '555-456-7890', 'Inactive', 6),
    (27, 'Elizabeth', 'Rodriguez', 'erodriguez27', 'pass', '10/04/1978', '555-567-8901', 'Active', 7),
    (28, 'Michael', 'Garcia', 'mgarcia28', 'pass', '17/09/1982', '555-678-9012', 'Inactive', 8),
    (29, 'Linda', 'Miller', 'lmiller29', 'pass', '06/12/1979', '555-789-0123', 'Active', 9),
    (30, 'William', 'Martinez', 'wmartinez30', 'pass', '22/03/1990', '555-890-1234', 'Inactive', 10);

    """

    cursor.execute(volunteer_data)

    refugee_data = """
    INSERT INTO refugees (refugeeID, first_name, last_name, date_of_birth, gender, familyID, campID, medical_condition,
    vital_status) VALUES
    (1, 'Jordan', 'Allen', '08/12/1946', 'Female', 645, 4, 'Asthma', 'Deceased'),
    (2, 'Liam', 'Brady', '16/06/1998', 'Female', 239, 15, 'Asthma', 'Alive'),
    (3, 'Louise', 'Harper', '05/09/1939', 'Female', 139, 5, 'Diabetes', 'Deceased'),
    (4, 'Gail', 'Khan', '02/06/2006', 'Male', 909, 15, 'Hypertension', 'Alive'),
    (5, 'Donna', 'Davis', '28/08/1992', 'Female', 834, 11, '', 'Alive'),
    (6, 'Sara', 'Jones', '10/11/2009', 'Female', 633, 16, 'Hypertension', 'Alive'),
    (7, 'George', 'Carr', '01/12/1930', 'Female', 171, 11, '', 'Alive'),
    (8, 'Max', 'Watson', '08/07/1990', 'Male', 572, 8, '', 'Alive'),
    (9, 'Megan', 'Williams', '07/06/1939', 'Male', 428, 1, 'Diabetes', 'Deceased'),
    (10, 'Simon', 'Davies', '02/11/1964', 'Male', 49, 14, 'None', 'Alive'),
    (11, 'Sian', 'Reid', '31/03/1987', 'Female', 119, 4, '', 'Alive'),
    (12, 'Allan', 'Miller', '27/12/1968', 'Female', 840, 15, 'Diabetes', 'Deceased'),
    (13, 'Gordon', 'Taylor', '19/02/1941', 'Male', 305, 5, 'Hypertension', 'Alive'),
    (14, 'Raymond', 'Allen', '03/01/1978', 'Male', 463, 10, 'Diabetes', 'Alive'),
    (15, 'Melanie', 'Taylor', '06/09/2022', 'Female', 19, 10, 'Diabetes', 'Alive'),
    (16, 'Shannon', 'Smith', '23/10/1947', 'Male', 6, 5, 'Diabetes', 'Alive'),
    (17, 'Jessica', 'Bailey', '21/10/1944', 'Female', 597, 3, 'Hypertension', 'Alive'),
    (18, 'Maria', 'Turner', '09/09/2005', 'Male', 516, 9, 'Asthma', 'Alive'),
    (19, 'Kim', 'Roberts', '16/10/2015', 'Male', 725, 12, 'Diabetes', 'Alive'),
    (20, 'Melissa', 'Schofield', '22/08/1956', 'Male', 71, 10, '', 'Deceased'),
    (21, 'Stephanie', 'Davies', '24/03/2023', 'Female', 788, 1, 'Asthma', 'Deceased'),
    (22, 'Gavin', 'Chapman', '06/04/1950', 'Female', 622, 6, '', 'Alive'),
    (23, 'Olivia', 'Leonard', '26/03/2021', 'Female', 462, 8, 'Hypertension', 'Alive'),
    (24, 'Elliot', 'Moore', '14/08/1934', 'Male', 747, 17, '', 'Alive'),
    (25, 'Rosemary', 'Johnson', '07/12/2020', 'Female', 971, 19, 'Diabetes', 'Alive'),
    (26, 'Kevin', 'Long', '15/04/1993', 'Male', 678, 10, 'Asthma', 'Deceased'),
    (27, 'Jonathan', 'Stevens', '05/11/1995', 'Male', 246, 20, '', 'Alive'),
    (28, 'Alexandra', 'Martin', '25/07/1979', 'Male', 176, 6, 'Hypertension', 'Alive'),
    (29, 'Dylan', 'Dixon', '18/09/2021', 'Male', 783, 19, '', 'Alive'),
    (30, 'Frank', 'Richards', '13/08/1981', 'Female', 862, 2, '', 'Alive'),
    (31, 'Ben', 'Owen', '05/07/2020', 'Female', 916, 13, 'Hypertension', 'Alive'),
    (32, 'Melanie', 'Bennett', '21/12/1938', 'Male', 140, 4, '', 'Alive'),
    (33, 'Hollie', 'Johnson', '17/03/1937', 'Male', 918, 5, '', 'Alive'),
    (34, 'Jonathan', 'Carroll', '11/11/1982', 'Male', 830, 8, 'Diabetes', 'Alive'),
    (35, 'Dawn', 'Harvey', '06/08/1959', 'Female', 182, 17, 'None', 'Alive'),
    (36, 'Shane', 'Lamb', '03/10/1962', 'Other', 228, 4, '', 'Alive'),
    (37, 'Callum', 'Smith', '27/07/1939', 'Male', 931, 14, 'Diabetes', 'Alive'),
    (38, 'Jade', 'Higgins', '15/09/1980', 'Female', 400, 7, '', 'Alive'),
    (39, 'Hazel', 'Cole', '08/09/1957', 'Male', 190, 16, 'None', 'Alive'),
    (40, 'Max', 'Stevens', '18/07/2018', 'Female', 40, 19, 'None', 'Alive'),
    (41, 'Raymond', 'Middleton', '21/07/2021', 'Female', 253, 19, 'Diabetes', 'Alive'),
    (42, 'Peter', 'Douglas', '20/08/1997', 'Female', 836, 17, 'None', 'Alive'),
    (43, 'Richard', 'Butcher', '10/01/1986', 'Male', 684, 8, 'Diabetes', 'Alive'),
    (44, 'Ross', 'Turner', '31/07/2005', 'Female', 616, 3, 'Hypertension', 'Alive'),
    (45, 'Hollie', 'Fraser', '19/09/1994', 'Male', 652, 10, 'None', 'Alive'),
    (46, 'Geraldine', 'Moran', '20/06/2016', 'Male', 209, 9, 'Diabetes', 'Alive'),
    (47, 'Diane', 'Bennett', '17/07/1945', 'Male', 442, 8, '', 'Alive'),
    (48, 'Aimee', 'Chadwick', '16/01/2003', 'Female', 785, 17, 'Hypertension', 'Alive'),
    (49, 'Cameron', 'Smith', '28/12/1931', 'Female', 35, 7, '', 'Alive'),
    (50, 'Catherine', 'Thomas', '24/01/1935', 'Male', 800, 6, 'Hypertension', 'Alive'),
    (51, 'Derek', 'Carter', '28/11/1985', 'Male', 237, 1, 'Asthma', 'Alive'),
    (52, 'Janet', 'OBrien', '31/07/1947', 'Male', 773, 2, '', 'Alive'),
    (53, 'Lee', 'Barnes', '01/08/1984', 'Male', 213, 15, 'Asthma', 'Alive'),
    (54, 'Marie', 'Bradley', '25/11/1958', 'Male', 189, 8, 'Diabetes', 'Alive'),
    (55, 'Sarah', 'Parker', '18/12/2009', 'Male', 154, 20, 'Asthma', 'Alive'),
    (56, 'Rachel', 'Elliott', '06/01/1925', 'Female', 474, 12, 'None', 'Deceased'),
    (57, 'Joseph', 'Fisher', '08/03/2011', 'Female', 418, 17, 'Hypertension', 'Alive'),
    (58, 'Wendy', 'Jones', '28/04/2021', 'Female', 380, 18, '', 'Alive'),
    (59, 'Martyn', 'Walker', '18/10/1973', 'Female', 41, 12, 'None', 'Alive'),
    (60, 'Elaine', 'Thomas', '11/04/1950', 'Female', 198, 2, 'Asthma', 'Alive'),
    (61, 'Rachel', 'Young', '22/04/2000', 'Male', 77, 5, 'None', 'Alive'),
    (62, 'Jeremy', 'Parry', '18/07/1951', 'Male', 986, 6, 'Hypertension', 'Alive'),
    (63, 'Elaine', 'Wilson', '13/11/2022', 'Male', 280, 20, 'Asthma', 'Alive'),
    (64, 'Karl', 'Begum', '22/06/1953', 'Male', 984, 1, 'Asthma', 'Alive'),
    (65, 'Louis', 'Coleman', '23/07/1990', 'Female', 416, 15, 'Diabetes', 'Alive'),
    (66, 'Angela', 'Thomas', '04/12/1986', 'Male', 789, 14, 'Diabetes', 'Alive'),
    (67, 'Lydia', 'Parker', '22/08/1996', 'Male', 527, 20, 'Asthma', 'Alive'),
    (68, 'Victoria', 'Whitehead', '30/06/2014', 'Male', 772, 8, 'Hypertension', 'Alive'),
    (69, 'Abigail', 'Gray', '23/08/1982', 'Male', 688, 16, '', 'Alive'),
    (70, 'Joe', 'Khan', '30/04/1959', 'Male', 852, 12, 'Hypertension', 'Alive'),
    (71, 'Holly', 'Hall', '09/04/2000', 'Female', 575, 8, 'None', 'Alive'),
    (72, 'Martin', 'Williams', '28/09/1975', 'Female', 437, 17, 'None', 'Alive'),
    (73, 'Antony', 'Ali', '12/02/1976', 'Female', 184, 20, 'Hypertension', 'Deceased'),
    (74, 'Carly', 'Jones', '08/05/1928', 'Female', 969, 16, '', 'Alive'),
    (75, 'Helen', 'Flynn', '15/01/2003', 'Female', 302, 13, 'Diabetes', 'Alive'),
    (76, 'Josh', 'Howard', '10/03/1985', 'Female', 243, 17, 'Diabetes', 'Deceased'),
    (77, 'Thomas', 'Taylor', '17/02/2015', 'Male', 817, 4, 'Asthma', 'Alive'),
    (78, 'Yvonne', 'Lyons', '24/08/1972', 'Male', 288, 4, 'None', 'Deceased'),
    (79, 'Liam', 'Grant', '01/05/1933', 'Female', 467, 5, '', 'Alive'),
    (80, 'Lesley', 'Cooper', '02/07/1975', 'Female', 423, 20, 'Diabetes', 'Deceased'),
    (81, 'Rachael', 'Jones', '25/11/1992', 'Female', 451, 18, 'None', 'Alive'),
    (82, 'Mohamed', 'Elliott', '14/05/1946', 'Female', 83, 8, 'None', 'Alive'),
    (83, 'Alexandra', 'Yates', '21/02/1981', 'Female', 16, 15, 'Asthma', 'Deceased'),
    (84, 'Bradley', 'Cooper', '21/03/1952', 'Male', 274, 3, 'Hypertension', 'Deceased'),
    (85, 'Shirley', 'Brown', '09/04/1986', 'Male', 47, 8, 'Diabetes', 'Alive'),
    (86, 'Justin', 'Read', '04/07/1925', 'Male', 569, 14, 'Asthma', 'Alive'),
    (87, 'Toby', 'Thompson', '17/05/1927', 'Female', 913, 2, 'None', 'Deceased'),
    (88, 'Garry', 'Robinson', '05/11/2009', 'Female', 279, 5, '', 'Alive'),
    (89, 'Adam', 'Taylor', '11/12/2002', 'Male', 979, 20, 'Diabetes', 'Alive'),
    (90, 'Yvonne', 'Page', '24/02/1945', 'Male', 261, 14, 'Hypertension', 'Alive'),
    (91, 'Darren', 'Harding', '11/02/1983', 'Male', 883, 3, 'Diabetes', 'Alive'),
    (92, 'Jodie', 'Johnson', '14/07/2007', 'Male', 119, 4, 'Asthma', 'Alive'),
    (93, 'Tracy', 'Page', '02/01/2003', 'Female', 76, 16, 'None', 'Alive'),
    (94, 'Edward', 'Woods', '01/12/2005', 'Male', 911, 3, 'Diabetes', 'Alive'),
    (95, 'Graeme', 'Parker', '17/09/1974', 'Male', 848, 10, 'None', 'Alive'),
    (96, 'Julie', 'Tucker', '18/04/1944', 'Other', 556, 10, 'Asthma', 'Alive'),
    (97, 'Hugh', 'Harris', '11/07/1989', 'Female', 365, 13, 'Hypertension', 'Alive'),
    (98, 'Marc', 'Brown', '08/09/2015', 'Female', 227, 8, '', 'Alive'),
    (99, 'Heather', 'Begum', '17/05/1962', 'Male', 443, 2, 'Hypertension', 'Alive'),
    (100, 'Joel', 'Wilkinson', '28/06/1925', 'Female', 383, 15, '', 'Alive');
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
