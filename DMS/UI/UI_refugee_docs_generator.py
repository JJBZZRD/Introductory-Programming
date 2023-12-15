from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.plan_data_retrieve import PlanDataRetrieve
import tkinter as tk
from tkinter import filedialog


def generate_refugee_document(root, refugee):
    refugee_details = (
        refugee
    )

    # Retrieve camp object
    camp_details = CampDataRetrieve.get_camp(campID=refugee.campID)[0]

    # The emergency contact is a volunteer at the same camp
    volunteer_contact = PersonDataRetrieve.get_volunteers(campID=refugee.campID)[0]

    # Retrieve plan details linked to the camp
    plan_details = PlanDataRetrieve.get_plan(planID=camp_details.planID)[0]

    family_members = PersonDataRetrieve.get_refugees(family_id=refugee.familyID)

    create_rtf_document(
        root, refugee_details, camp_details, volunteer_contact, family_members
    )


def create_rtf_document(
    root, refugee_details, camp_details, volunteer_contact, family_members
):
    file_path = filedialog.asksaveasfilename(
        initialdir="/",
        initialfile=f"refugee_document_{refugee_details.refugeeID}_{refugee_details.first_name}_{refugee_details.last_name}.rtf",
        defaultextension=".rtf",
        filetypes=[("RTF files", "*.rtf")],
        parent=root,
    )

    if not file_path:
        return

    rtf_template = r"{\rtf1\ansi{\fonttbl\f0\fswiss Helvetica;}\f0\pard"

    def add_text(text, bold=False, newline=True):
        formatted_text = r"\b " + text + r"\b0 " if bold else text
        if newline:
            formatted_text += r"\par"
        return formatted_text

    rtf_content = rtf_template

    title = f"Refugee Documentation: ID {refugee_details.refugeeID} - {refugee_details.first_name} {refugee_details.last_name}"
    rtf_content += add_text(title, bold=True)

    rtf_content += add_text("Personal Information", bold=True)
    rtf_content += add_text("\nRefugee ID: " + str(refugee_details.refugeeID))
    rtf_content += add_text(
        "\nFull Name: " + refugee_details.first_name + " " + refugee_details.last_name
    )
    rtf_content += add_text("\nDate of Birth: " + str(refugee_details.date_of_birth))
    rtf_content += add_text("\nGender: " + refugee_details.gender)
    rtf_content += add_text(
        "\nMedical Condition: " + refugee_details.medical_conditions
    )
    rtf_content += add_text("\nVital Status: " + refugee_details.vital_status)
    rtf_content += add_text("\n")
    rtf_content += add_text("\nCamp Assignment", bold=True)
    rtf_content += add_text("\nCamp ID: " + str(camp_details.campID))
    rtf_content += add_text("\nCamp Name: " + camp_details.location)
    rtf_content += add_text("\n")

    if family_members:
        rtf_content += add_text("\nFamily Members:", bold=True)
        for member in family_members:
            rtf_content += add_text(
                str(member.refugeeID) + " " + member.first_name + " " + member.last_name
            )

    rtf_content += add_text("\n")
    rtf_content += add_text("Emergency Contact Information", bold=True)
    rtf_content += add_text(
        "\nEmergency Contact: "
        + volunteer_contact.first_name
        + " "
        + volunteer_contact.last_name
        + ", "
        + str(volunteer_contact.phone)
    )

    rtf_content += "}"

    with open(file_path, "w") as file:
        file.write(rtf_content)
