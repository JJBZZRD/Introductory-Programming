from config import conn, cursor


def insert_dummy_data():
    plans_data = """
    INSERT INTO plans (planID, start_date, end_date, name, region, event_name, description) VALUES
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
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina",
    "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
    "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana",
    "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Côte d'Ivoire", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
    "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (Swaziland)", "Ethiopia",
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada",
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See (Vatican City State)", "Honduras",
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
    "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine (State of)", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia",
    "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland",
    "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States",
    "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe";
    """

    cursor.execute(insert_countries)

    conn.commit()


insert_dummy_data()

conn.close()