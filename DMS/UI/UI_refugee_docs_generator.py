
from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.plan_data_retrieve import PlanDataRetrieve

def generate_refugee_document(refugee):
    refugee_details = PersonDataRetrieve.get_refugees(id=refugee.refugeeID)[0]

    # Retrieve camp details
    camp_details = CampDataRetrieve.get_camp(campID=refugee.campID)

    # The emergency contact is a volunteer at the same camp
    volunteer_contact = PersonDataRetrieve.get_volunteers(campID=refugee.campID)[0]  

    # Retrieve plan details linked to the camp
    plan_details = PlanDataRetrieve.get_plan(planID=camp_details[0].planID)

    # family_members = get_family_members(refugee_details['familyID'])

    create_rtf_document(refugee_details, camp_details, volunteer_contact, family_members)


def create_rtf_document(refugee_details, camp_details, volunteer_contact, family_members):
    rtf_template = r"{\rtf1\ansi{\fonttbl\f0\fswiss Helvetica;}\f0\pard"

    def add_text(text, bold=False, newline=True):
        formatted_text = r"\b " + text + r"\b0 " if bold else text
        if newline:
            formatted_text += r"\par"
        return formatted_text

    rtf_content = rtf_template

    title = f"Refugee Documentation: ID {refugee_details.refugeeID} - {refugee_details.first_name} + ' ' + {refugee_details.last_name}"
    rtf_content += add_text(title, bold=True)

    rtf_content += add_text("Personal Information", bold=True)
    rtf_content += add_text("Refugee ID: " + refugee_details.refugeeID)
    rtf_content += add_text("Full Name: " + refugee_details.first_name + ' ' + refugee_details.last_name)
    rtf_content += add_text("Date of Birth: " + refugee_details.date_of_birth)
    rtf_content += add_text("Gender: " + refugee_details.gender)
    rtf_content += add_text("Medical Condition: " + refugee_details.medical_conditions)
    rtf_content += add_text("Vital Status: " + refugee_details.vital_status)
    
    rtf_content += add_text("Camp Assignment", bold=True)
    rtf_content += add_text("Camp ID: " + camp_details.campID)
    rtf_content += add_text("Camp Location: " + camp_details.location)

    if family_members:
        rtf_content += add_text("Family Members:", bold=True)
        for member in family_members:
            rtf_content += add_text(member['name'] + " (" + member['relationship'] + ")")

    rtf_content += add_text("Emergency Contact Information", bold=True)
    rtf_content += add_text("Emergency Contact: " + volunteer_contact['name'] + ", " + volunteer_contact['phone'])

    rtf_content += "}"

    filename = f"refugee_document_{refugee_details['refugeeID']}_{refugee_details['full_name']}.rtf"
    with open(filename, "w") as file:
        file.write(rtf_content)

refugee_details = {
    'refugeeID': '12345',
    'full_name': 'John Doe',
    'date_of_birth': '01/01/1980',
    'gender': 'Male',
    'medical_conditions': 'None',
    'vital_status': 'Alive'
}

camp_details = {
    'campID': 'C001',
    'location': 'Camp Location'
}

volunteer_contact = {
    'name': 'Jane Smith',
    'phone': '555-0101'
}

family_members = [
    {'name': 'Jane Doe', 'relationship': 'Spouse'},
    {'name': 'Baby Doe', 'relationship': 'Child'}
]

create_rtf_document(refugee_details, camp_details, volunteer_contact, family_members)
