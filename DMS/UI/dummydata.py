from random import randint, choice
from datetime import datetime, timedelta
import string

class Refugee:  # Refugee class has attributes matching columns in table
    def __init__(self, refugeeID, first_name, last_name, date_of_birth, familyID, campID, medical_condition):
        self.refugeeID = refugeeID
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.familyID = familyID
        self.campID = campID
        self.medical_condition = medical_condition  

refugee1 = Refugee(1,"wobtvhed", "fiimtukd", "1991-01-23 00:00:00", "ejhafm", 1, "Critical")
refugee2 = Refugee(2,"qhmdapsb", "rcwhasup", "1961-01-21 00:00:00", "fwgpga", 1, "None")
refugee3 = Refugee(3,"vbyrjkeo", "pufhahjg", "1973-03-19 00:00:00", "wmrrly", 1, "None")
refugee4 = Refugee(4,"itfebyvd", "jmctrrqn", "1975-01-12 00:00:00", "wfmpne", 1, "None")
refugee5 = Refugee(5,"fyngllcj", "ezyegffu", "1968-06-21 00:00:00", "isamqs", 1, "None")
refugee6 = Refugee(6,"jkugfesq", "khczusdj", "1987-02-23 00:00:00", "wjnknc", 1, "Critical")
refugee7 = Refugee(7,"suuhtoal", "mgldzolb", "2006-05-05 00:00:00", "yrhjhf", 2, "Minor")
refugee8 = Refugee(8,"jvbwqukr", "ktalmptr", "1984-05-11 00:00:00", "zvfmwk", 2, "None")
refugee9 = Refugee(9,"asnwbqiq", "xrhqnhfb", "2007-06-20 00:00:00", "eaikat", 2, "None")
refugee10 = Refugee(10,"jucdvnai", "eqgyipfj", "1986-06-14 00:00:00", "kllyyp", 2, "Minor")
refugee11 = Refugee(11,"vkmpwcur", "iamgcgrg", "1977-08-14 00:00:00", "drtubt", 2, "None")
refugee12 = Refugee(12,"sunoozgw", "tcdhynpu", "1980-04-30 00:00:00", "ufrrpm", 2, "Critical")
refugee13 = Refugee(13,"llzjyilb", "yjstjesn", "1987-07-20 00:00:00", "cdmtpu", 3, "Critical")
refugee14 = Refugee(14,"bwbsngpj", "jtyfxbej", "1970-06-19 00:00:00", "suultu", 3, "None")
refugee15 = Refugee(15,"fotlqjbt", "gmilnkqu", "2009-01-15 00:00:00", "zcdbpe", 3, "None")
refugee16 = Refugee(16,"ddnrxxqy", "cylhmzhd", "1993-10-30 00:00:00", "jdeklt", 3, "None")
refugee17 = Refugee(17,"tzwhxmof", "mthiutxz", "1996-12-24 00:00:00", "isfphb", 3, "None")
refugee18 = Refugee(18,"dhltqork", "njwbsaxv", "1969-07-15 00:00:00", "quhhpj", 3, "Minor")
refugee19 = Refugee(19,"rxgvdumz", "dpyeanwc", "1977-12-07 00:00:00", "fjlwtk", 3, "Minor")
refugee20 = Refugee(20,"bgftrgip", "taionuey", "1967-02-19 00:00:00", "pgicmw", 3, "Minor")
refugee21 = Refugee(21,"kwipjkmq", "tprwanij", "1975-01-10 00:00:00", "duikyw", 3, "Minor")
refugee22 = Refugee(22,"bhmmpwlk", "nmzioozj", "1978-12-10 00:00:00", "sedzkc", 3, "Minor")
refugee23 = Refugee(23,"ueklafhx", "zzkllmxj", "1999-12-06 00:00:00", "ixxhxb", 3, "None")
refugee24 = Refugee(24,"tuhqikvg", "hwsejxan", "2003-03-16 00:00:00", "wxhcji", 3, "None")
refugee25 = Refugee(25,"eghiidaf", "mswbrffr", "2004-10-22 00:00:00", "yuextm", 3, "Critical")
refugee26 = Refugee(26,"uirqjmyc", "qyuvtnfi", "2003-07-10 00:00:00", "fcjaox", 4, "Minor")
refugee27 = Refugee(27,"agyixnsw", "nnmfznjs", "1996-03-25 00:00:00", "pmaphu", 4, "None")
refugee28 = Refugee(28,"uubdajon", "sugwtelk", "2008-06-13 00:00:00", "ufvyma", 4, "Minor")
refugee29 = Refugee(29,"ymewmblz", "gymvdnwt", "1985-03-19 00:00:00", "tnfgnb", 4, "Minor")
refugee30 = Refugee(30,"faofdviq", "xnythyoh", "1986-07-18 00:00:00", "rgyknt", 4, "Critical")
refugee31 = Refugee(31,"umdhgefb", "bxyhnrum", "1963-05-19 00:00:00", "ahrnmb", 4, "Critical")
refugee32 = Refugee(32,"dzyptcoa", "hzdsrqta", "2003-06-01 00:00:00", "asmwyq", 4, "Critical")
refugee33 = Refugee(33,"azwjvmso", "duhondzx", "1995-03-31 00:00:00", "lnmeoe", 4, "Critical")
refugee34 = Refugee(34,"tfzonkqo", "tlrpmphn", "1982-02-14 00:00:00", "hmcbwv", 5, "None")
refugee35 = Refugee(35,"birkelzn", "nfcalxgn", "1998-09-11 00:00:00", "fvjvxq", 5, "None")
refugee36 = Refugee(36,"bofcwzcp", "trybbilo", "1992-11-27 00:00:00", "egvnrt", 5, "None")
refugee37 = Refugee(37,"wekxfwsh", "sxcubdxk", "1964-06-15 00:00:00", "cywqjo", 5, "None")
refugee38 = Refugee(38,"uhtkxzra", "sjyjadgq", "1977-05-16 00:00:00", "cccjna", 5, "None")
refugee39 = Refugee(39,"awqwyvyi", "rlqersqy", "1994-05-04 00:00:00", "ygenik", 5, "Critical")
refugee40 = Refugee(40,"emxhhtqp", "zvoqakjj", "1983-02-20 00:00:00", "iqclbj", 5, "Minor")
refugee41 = Refugee(41,"vwldkgrm", "obdrkmav", "1999-10-10 00:00:00", "osclpm", 5, "Critical")
refugee42 = Refugee(42,"qckrjgti", "pdwjorrc", "1983-05-28 00:00:00", "lfndhe", 5, "Critical")
refugee43 = Refugee(43,"avgagtba", "gxntgfau", "1961-07-12 00:00:00", "cllqwp", 5, "Minor")
refugee44 = Refugee(44,"yigumxnq", "neeogqpj", "1983-10-28 00:00:00", "cngdym", 5, "Critical")
refugee45 = Refugee(45,"gjljcvac", "hplushqc", "2005-06-01 00:00:00", "vehpoy", 5, "Critical")
refugee46 = Refugee(46,"gzdgzjft", "uksyxxgn", "1998-02-09 00:00:00", "zwgozj", 5, "Critical")
refugee47 = Refugee(47,"fuskviwf", "ibfzjamt", "1979-06-27 00:00:00", "eogbyd", 5, "None")
refugee48 = Refugee(48,"bbwrakhj", "ucxjkwmd", "2005-06-16 00:00:00", "fxoaxm", 6, "Minor")
refugee49 = Refugee(49,"wcawcusr", "rgfzmcth", "1995-03-28 00:00:00", "nadlqf", 6, "None")
refugee50 = Refugee(50,"rbiytbds", "wbslzyfj", "1979-10-13 00:00:00", "htspef", 6, "Critical")
refugee51 = Refugee(51,"fzctntfk", "vhonemls", "2000-04-12 00:00:00", "fzxakz", 6, "None")
refugee52 = Refugee(52,"sjtfpdxl", "ylthlhwc", "1966-10-23 00:00:00", "wbaogy", 6, "Critical")
refugee53 = Refugee(53,"lqsukhit", "cmktdhiw", "1973-05-25 00:00:00", "pyqscp", 6, "Minor")
refugee54 = Refugee(54,"nyqjondn", "tfpyuzxe", "2005-08-25 00:00:00", "fofgwk", 6, "Minor")
refugee55 = Refugee(55,"vxshsdhe", "gtxpnrjk", "1984-07-15 00:00:00", "celnod", 6, "Minor")
refugee56 = Refugee(56,"ivdoxxtw", "sfkfgrqv", "1996-07-28 00:00:00", "uyscnl", 6, "Critical")
refugee57 = Refugee(57,"cvdimram", "rwtnhqjs", "1977-04-09 00:00:00", "fdnsxx", 6, "Minor")
refugee58 = Refugee(58,"bnfpvxff", "xkeikhja", "1964-03-08 00:00:00", "sasmiu", 6, "None")
refugee59 = Refugee(59,"timzoxsx", "uwyqeavw", "2000-05-15 00:00:00", "wxkley", 6, "None")
refugee60 = Refugee(60,"tmjklfkp", "ghfydhbv", "1970-10-27 00:00:00", "xstjsl", 6, "None")
refugee61 = Refugee(61,"kfkvlmcn", "lilpsvir", "1978-01-05 00:00:00", "kgsurz", 6, "None")

class Plan:  # Plan class has attributes matching columns in table
    def __init__(self, planID, start_date, end_date, name, region, event_name, description):
        self.planID = planID
        self.start_date = start_date
        self.end_date = end_date
        self.region = region
        self.name = name
        self.event_name = event_name
        self.description = description


    def get_info(self):
        return [self.planID, self.name, self.region, self.event_name, self.description, self.start_date, self.end_date]

plan1 = Plan(1,"2021-04-06 00:00:00", "2024-11-05 00:00:00", 1, "llpbfkwc", "kejwwboo", "hojngythjcbrknhwxngu")
plan2 = Plan(2,"2022-11-24 00:00:00", "2025-03-20 00:00:00", 2, "musqqfqi", "ndcxysnm", "juuaeanpfylklqyeawqp")

class Camp:  # Camp class has attributes matching columns in table
    def __init__(self, campID, location, shelter,max_shelter, water, max_water, food, max_food, medical_supplies,
                 max_medical_supplies, planID):
        self.campID = campID
        self.location = location
        self.shelter = shelter
        self.max_shelter = max_shelter
        self.water = water
        self.max_water = max_water
        self.food = food
        self.max_food = max_food
        self.medical_supplies = medical_supplies
        self.max_medical_supplies = max_medical_supplies
        self.planID = planID 

camp1 = Camp(1, 'france',330, 390,2064, 5588, 1751, 8266, 169, 640, 1)
camp2 = Camp(2, 'japan', 480, 560,1741, 6238, 4373, 5147, 367, 903, 1)
camp3 = Camp(3, 'US', 466, 560, 3995,7022, 1547, 9832, 435, 978, 1)
camp4 = Camp(4, 'Germany',310, 320,2066, 5510, 4763, 8174, 359, 829, 2)
camp5 = Camp(5, 'Italy',485, 340,1975, 8688, 2961, 7004, 386, 749, 2)
camp6 = Camp(6, 'Dundee',428, 570,4698, 8122, 2632, 7277, 435, 510, 2)

class Volunteer:
    def __init__(self, volunteerID, first_name, last_name, username, password, date_of_birth, phone, account_status, campID):
        self.volunteerID = volunteerID
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.account_status = account_status
        self.campID = campID

volunteer1 = Volunteer(1,"Tim", "ypmzjxuh", "ortrhnth", "wgyxmdpg", "1975-01-16 00:00:00", "6585437408", "active", 1)
volunteer2 = Volunteer(2,"dog", "azopxnlf", "ncyzwkdp", "xqbyrfsv", "1986-05-15 00:00:00", "6973412354", "active", 2)
volunteer3 = Volunteer(3,"the meadows monster", "jxnkmwcm", "lgyszshp", "wimcislw", "1987-07-02 00:00:00", "2983196720", "inactive", 3)
volunteer4 = Volunteer(4, "johnny sandbag", "dbrtjpwi", "vthevtvn", "dvtvhdmw", "1985-02-02 00:00:00", "8128297929", "active", 4)
volunteer5 = Volunteer(5, "the ghost of christmas past","vwixpijq", "ayzwbqir", "tiyownvj", "1990-04-21 00:00:00", "7287360101", "inactive", 5)
volunteer6 = Volunteer(6, "Jacque Ceastau","atwepvgk", "vhtrihat", "ckxgmrpy", "1975-04-06 00:00:00", "4143230804", "active", 6)
        
class Admin:
    def __init__(self, adminID, first_name, last_name, username, date_of_birth, password, phone):
        self.adminID = adminID
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.date_of_birth = date_of_birth
        self.phone = phone 

admin = Admin(1,"Jimothy","James", "cgffoivg", "ktxmpddc", "1960-02-26 00:00:00", "8226116235")


def random_string(length=8):
    """Generate a random string of fixed length."""
    return ''.join(choice(string.ascii_lowercase) for i in range(length))

def random_date(start, end):
    """Generate a random date between two dates."""
    return start + timedelta(days=randint(0, int((end - start).days)))

def generate_dummy_data():
    # Generate data for one Admin
    admin = {
        "first_name": random_string(),
        "last_name": random_string(),
        "username": random_string(),
        "date_of_birth": str(random_date(datetime(1960, 1, 1), datetime(2000, 1, 1))),
        "password": random_string(),
        "phone": ''.join([str(randint(0, 9)) for _ in range(10)])
    }

    # Generate data for two Plans
    plans = []
    for _ in range(2):
        plans.append({
            "start_date": str(random_date(datetime(2020, 1, 1), datetime(2023, 1, 1))),
            "end_date": str(random_date(datetime(2024, 1, 1), datetime(2026, 1, 1))),
            "name": random_string(),
            "region": random_string(),
            "event_name": random_string(),
            "description": random_string(20)
        })

    # Generate data for Camps and Volunteers
    camps = []
    volunteers = []
    for plan in plans:
        for _ in range(3):
            camp = {
                "location": random_string(),
                "max_shelter": randint(100, 500),
                "water": randint(1000, 5000),
                "max_water": randint(5000, 10000),
                "food": randint(1000, 5000),
                "max_food": randint(5000, 10000),
                "medical_supplies": randint(100, 500),
                "max_medical_supplies": randint(500, 1000),
                "planID": plan["name"]
            }
            camps.append(camp)

            volunteer = {
                "first_name": random_string(),
                "last_name": random_string(),
                "username": random_string(),
                "password": random_string(),
                "date_of_birth": str(random_date(datetime(1960, 1, 1), datetime(2000, 1, 1))),
                "phone": ''.join([str(randint(0, 9)) for _ in range(10)]),
                "account_status": choice(["active", "inactive"]),
                "campID": camp["location"]
            }
            volunteers.append(volunteer)

    refugees = []
    for camp in camps:
        for _ in range(randint(5, 15)):  # Random number of refugees per camp
            refugee = {
                "first_name": random_string(),
                "last_name": random_string(),
                "date_of_birth": str(random_date(datetime(1960, 1, 1), datetime(2010, 1, 1))),
                "familyID": random_string(6),
                "campID": camp["location"],
                "medical_condition": choice(["None", "Minor", "Critical"])
            }
            refugees.append(refugee)

    # Instantiate Admin
    admin_obj = Admin(**admin)

    # Instantiate Plans
    plan_objs = [Plan(**plan) for plan in plans]

    # Instantiate Camps
    camp_objs = [Camp(**camp) for camp in camps]

    # Instantiate Volunteers
    volunteer_objs = [Volunteer(**volunteer) for volunteer in volunteers]

    # Instantiate Refugees
    refugee_objs = [Refugee(**refugee) for refugee in refugees]

    return admin_obj, plan_objs, camp_objs, volunteer_objs, refugee_objs

def save_objects_to_file(filename, admin, plans, camps, volunteers, refugees):
    with open(filename, 'w') as file:
        file.write("from your_module import Admin, Plan, Camp, Volunteer, Refugee\n\n")  # Replace 'your_module' with the actual module name

        # Write Admin
        admin_attrs = [quote_str(admin.first_name), quote_str(admin.last_name), quote_str(admin.username), quote_str(admin.password), quote_str(admin.date_of_birth), quote_str(admin.phone)]
        file.write(f"admin = Admin({', '.join(admin_attrs)})\n\n")

        # Write Plans
        for i, plan in enumerate(plans):
            plan_attrs = [quote_str(plan.start_date), quote_str(plan.end_date), quote_str(plan.name), quote_str(plan.region), quote_str(plan.event_name), quote_str(plan.description)]
            file.write(f"plan{i+1} = Plan({', '.join(plan_attrs)})\n")

        file.write("\n")

        # Write Camps
        for i, camp in enumerate(camps):
            camp_attrs = [quote_str(camp.location), camp.max_shelter, camp.water, camp.max_water, camp.food, camp.max_food, camp.medical_supplies, camp.max_medical_supplies, quote_str(camp.planID)]
            file.write(f"camp{i+1} = Camp({', '.join(map(str, camp_attrs))})\n")

        file.write("\n")

        # Write Volunteers
        for i, volunteer in enumerate(volunteers):
            volunteer_attrs = [quote_str(volunteer.first_name), quote_str(volunteer.last_name), quote_str(volunteer.username), quote_str(volunteer.password), quote_str(volunteer.date_of_birth), quote_str(volunteer.phone), quote_str(volunteer.account_status), quote_str(volunteer.campID)]
            file.write(f"volunteer{i+1} = Volunteer({', '.join(volunteer_attrs)})\n")

        file.write("\n")

        # Write Refugees
        for i, refugee in enumerate(refugees):
            refugee_attrs = [quote_str(refugee.first_name), quote_str(refugee.last_name), quote_str(refugee.date_of_birth), quote_str(refugee.familyID), quote_str(refugee.campID), quote_str(refugee.medical_condition)]
            file.write(f"refugee{i+1} = Refugee({', '.join(refugee_attrs)})\n")

        file.write("\n")

def quote_str(s):
    """Enclose a string in quotes for Python syntax."""
    return f'"{s}"' if isinstance(s, str) else s

# # Generate the dummy data
# admin, plans, camps, volunteers, refugees = generate_dummy_data()

# # Save the objects to a new Python file
# save_objects_to_file('generated_objects.py', admin, plans, camps, volunteers, refugees)









