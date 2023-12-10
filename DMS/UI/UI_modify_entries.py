import tkinter as tk
from tkinter import ttk
from ..Logic.camp_data_edit import CampDataEdit
from ..Logic.plan_data_edit import PlanEdit
from ..Logic.person_data_edit import PersonDataEdit
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.plan_data_retrieve import PlanDataRetrieve
from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..DB.countries import get_all_countries

# the name of this class might not explain the functionality very well as its quite an abstraction. This class
# produces varients of the pages to modfiy camps, plans, refugees, volunteers (and admins as personal details) There
# will be two varients for each subclass. adding new records and modfiying existing records
class ModifyEntries(tk.Frame):
    def __init__(self, ui_manager, **kwargs):
        super().__init__(ui_manager.root, **kwargs)
        self.root = ui_manager.root
        self.screen_data = ui_manager.screen_data
        self.show_screen = ui_manager.show_screen
        self.page_nav = ui_manager.page_nav
        self.logged_in_user = ui_manager.logged_in_user
        self.lower_frame = None
        self.modify_type = None  # this passes the title name information from the subclass to the 'def create_title(self):' method
        self.modifiable_variables: list = []  # this allows the subclass to pass the list of entry names to the ' def create_entry_fields(self):' method
        self.current_data = []  # this information is passed to be displayed in the entry fields only if it is an edit entry variant subclass being called
        self.entry_fields = {}  # this variable creates a dictionary that allows you to extract the values from the entry fields in 'def create_entry_fields(self):'
        self.filter_matching = {}
        self.button_labels = None
        self.create_record = None
        self.save_record = None
        self.delete_record = None
        self.deactivate_record = None
        self.button_list = {}
        self.button_column = None
        self.fields_to_be_dropdown = {}
        self.read_only_fields = []
        self.setup_modify()

    def setup_modify(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different entry modify pages")

    def create_title(self):
        # this method creates the title
        # page_top_frame = tk.Frame(self.root)
        # page_top_frame.pack(side='top')

        modify_title = ttk.Label(self, text=self.modify_type[0], font=("Helvetica", 20, "bold"))
        modify_title.pack(side='top', padx=10, pady=5)

    def create_entry_fields(self):
        # lower_frame = tk.Frame(self)
        self.lower_frame.pack(pady=10)
        entry_fields = {}
        # The ui logic to display the current values from the database within the entry boxes (read-only or
        # otherwise) is held in the following for loop

        k = 1
        j = 0
        for i, variable in enumerate(self.modifiable_variables):  # this loop creates a vertical list of columns that is 4 high maximum
            if variable in self.fields_to_be_dropdown:
                entry_name = ttk.Label(self.lower_frame, text=variable)
                entry_name.grid(column=k, row=j, pady=5, padx=5)

                drop_down = ttk.Combobox(self.lower_frame, values=self.fields_to_be_dropdown[variable], state='readonly')

                if self.current_data is not None and i < len(self.current_data):
                    drop_down.set(self.current_data[i])
                else:
                    drop_down.set(self.fields_to_be_dropdown[variable][0])
                drop_down.grid(column=k + 1, row=j, pady=5, padx=5)
                self.entry_fields.update({variable: [self.filter_matching[variable], drop_down]})
            else:
                entry_name = ttk.Label(self.lower_frame, text=variable)
                entry_name.grid(column=k, row=j, pady=5, padx=5)

                entry_field = ttk.Entry(self.lower_frame)
                entry_field.grid(column=k + 1, row=j, pady=5, padx=5)

                self.entry_fields.update({variable: [self.filter_matching[variable], entry_field]})

                if self.current_data is not None and i < len(self.current_data):
                    placeholder = self.current_data[i]
                elif "Date" in variable:
                    placeholder = "yyyy-mm-dd"
                else:
                    placeholder = "Enter " + variable

                entry_field.insert(0, placeholder)
                entry_field.bind("<FocusIn>", lambda event, e=entry_field, p=placeholder: self.on_focus_in(event, e, p))
                entry_field.bind("<FocusOut>", lambda event, e=entry_field, p=placeholder: self.on_focus_out(event, e, p))
    
            

            if j == 3:
                k += 2
                j = -1

            j += 1
            self.button_column = k + 2

    def on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def on_focus_out(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)

    def create_buttons(self):
        #save_record = ttk.Button(self.lower_frame, text=self.button_labels[0], command=self.on_click_save_record)
        #save_record.grid(column=5, row=4, padx=5, pady=5)
        # if self.display_delete_button:
        #     save_record = ttk.Button(self.lower_frame, text=self.button_labels[1], command=self.on_click_save_record)
        #     save_record.grid(column=5, row=3, padx=5, pady=5)
        #
        for i, button in enumerate(self.button_labels):
            new_button = ttk.Button(self.lower_frame, text=button, command=lambda b=button: self.button_click_function(b))
            new_button.grid(column=self.button_column, row=4-i, padx=5, pady=5)
            self.button_list.update({button: new_button})

        spacer_button = ttk.Button(self.lower_frame, text=self.button_labels[0])
        spacer_button.grid()

        spacer_width = spacer_button.winfo_reqwidth() + 10

        spacer_button.grid_forget()

        spacer_frame = ttk.Frame(self.lower_frame, height=0, width=spacer_width)
        spacer_frame.grid(column=0, row=4)

    def button_click_function(self, button):

        match button:
            case 'Save Changes':
                inputs = {}
                for key in self.entry_fields:
                    inputs.update({self.entry_fields[key][0]: self.entry_fields[key][1].get()})
                #print(tuple(inputs))

                self.save_record(**inputs)
                # try to update data using the business logic function

            case 'Delete':

                # logic for deleting object passed into screen data

                pass
            case 'Deactivate':

                # logic for deactivating volunteer account
                pass
            case 'Create':
                inputs = {}
                for key in self.entry_fields:
                    inputs.update({self.entry_fields[key][0]: self.entry_fields[key][1].get()})
                #print(tuple(inputs))

                self.create_record(**inputs)
                self.page_nav('back')
                # logic for creating object
                pass
            case 'End':

                # logic fo r ending a plan
                pass

        # takes the entry field values




        # if returns true 
        # return success message utility

        # if returns list
        # return error message utility with error list as input?


class NewPlan(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Plan']
        self.modifiable_variables = ['Plan Name', 'Event Name', 'Country', 'Description', 'Start Date', 'End Date']
        self.filter_matching = {'Plan ID': 'planID', 'Plan Name': 'name', 'Country': 'country', 'Event Name': 'event_name',
                                'Description': 'description', 'Start Date': 'start_date', 'End Date': 'end_date'}
        self.button_labels = ['Create']
        self.current_data = None
        self.create_record = PlanEdit.create_plan
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Country': get_all_countries()}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditPlan(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Plan']
        self.modifiable_variables = ['Plan ID', 'Plan Name', 'Country', 'Event Name', 'Description', 'Start Date', 'End Date']
        self.filter_matching = {'Plan ID': 'planID', 'Plan Name': 'name', 'Country': 'country', 'Event Name': 'event_name',
                                'Description': 'description', 'Start Date': 'start_date', 'End Date': 'end_date'}
        self.button_labels = ['Save Changes', 'End', 'Delete']
        self.current_data = self.screen_data.display_info()
        self.save_record = PlanEdit.update_plan
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Country': get_all_countries()}
        self.read_only_fields = ['Plan ID']
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class NewCamp(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Camp']
        self.modifiable_variables = ['Country', 'Max Shelter', 'Water', 'Max Water', 'Food', 'Max_Food',
                             'Medical Supplies', 'Max Medical Supplies', 'Plan ID']
        self.filter_matching = {'Camp ID': 'campID', 'Country': 'location', 'Max Shelter': 'max_shelter', 'Water': 'water', 'Max Water': 'max_water', 'Food': 'food', 'Max_Food': 'max_food',
                                'Medical Supplies': 'medical_supplies', 'Max Medical Supplies': 'max_medical_supplies', 'Plan ID': 'planID'}
        self.button_labels = ['Create']
        self.save_record = CampDataEdit.create_camp
        self.entry_fields = {}
        self.read_only_fields = []
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditCamp(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Camp']
        self.modifiable_variables = ['Camp ID', 'Country', 'Max Shelter', 'Water', 'Max Water', 'Food', 'Max_Food',
                             'Medical Supplies', 'Max Medical Supplies', 'Plan ID']
        self.filter_matching = {'Camp ID': 'campID', 'Country': 'location', 'Max Shelter': 'max_shelter', 'Water': 'water', 'Max Water': 'max_water', 'Food': 'food', 'Max_Food': 'max_food',
                                'Medical Supplies': 'medical_supplies', 'Max Medical Supplies': 'max_medical_supplies', 'Plan ID': 'planID'}
        self.current_data = self.screen_data.display_info()
        self.button_labels = ['Save Changes', 'Delete']
        self.save_record = CampDataEdit.update_camp
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Plan ID': [plan.PlanID for plan in PlanDataRetrieve.get_all_plans()]}
        self.read_only_fields = ['Plan ID']
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class NewVolunteer(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Volunteer']
        self.modifiable_variables = ['Volunteer ID', 'First Name', 'Last Name', 'Username',
                'Date of Birth', 'Phone', 'Account Status', 'Camp ID']
        self.filter_matching = {'Volunteer ID': 'volunteerID', 'First Name': 'name', 'Last Name': 'name', 'Username': 'username',
                'Date of Birth': 'date_of_birth', 'Phone': 'phone', 'Camp ID': 'campID', 'Account Status': 'account_status'}
        self.button_labels = ['Create']
        # self.display_delete_button = False
        self.save_record = PersonDataEdit.create_volunteer
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Camp ID': [camp.campID for camp in CampDataRetrieve.get_all_camps()]}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditVolunteer(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Volunteer']
        self.modifiable_variables = ['Volunteer ID', 'First Name', 'Last Name', 'Username',
                'Date of Birth', 'Phone', 'Account Status', 'Camp ID']
        self.filter_matching = {'Volunteer ID': 'volunteerID', 'First Name': 'name', 'Last Name': 'name', 'Username': 'username',
                'Date of Birth': 'date_of_birth', 'Phone': 'phone', 'Camp ID': 'campID', 'Account Status': 'account_status'}
        self.button_labels = ['Save Changes', 'Deactivate']
        self.current_data = self.screen_data.display_info()
        self.save_record = PersonDataEdit.update_volunteer
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()
        # print(self.entry_fields)


class NewRefugee(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Refugee']
        self.modifiable_variables = ['Refugee ID', 'First Name', 'Last Name',
                'Date of_Birth', 'Gender', 'Family ID',
                'Camp ID', 'Triage Category', 'Medical Conditions',
                'Vital Status']
        self.filter_matching = {'Refugee ID': 'id', 'First Name': 'name', 'Last Name': 'name',
                'Date of_Birth': 'date_of_birth', 'Gender': 'gender', 'Family ID': 'family_id',
                'Camp ID': 'camp_id', 'Triage Category': 'triage_category', 'Medical Conditions': 'medical_condition',
                'Vital Status': 'vital_status'}
        self.fields_to_be_dropdown = {'Camp ID': [camp.campID for camp in CampDataRetrieve.get_all_camps()], 'Vital Status': ['Alive', 'Deceased'], 
                                      'Gender': ['Male', 'Female', 'Other'], 'Triage Category': ['None', 'Non-Urgent', 'Standard', 'Urgent', 'Very-Urgent', 'Immediate']}
        self.button_labels = ['Create']
        self.save_record = PersonDataEdit.create_refugee
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditRefugee(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['View/Edit Refugee']
        self.modifiable_variables = ['Refugee ID', 'First Name', 'Last Name',
                'Date of_Birth', 'Gender', 'Family ID',
                'Camp ID', 'Triage Category', 'Medical Conditions',
                'Vital Status']
        self.filter_matching = {'Refugee ID': 'id', 'First Name': 'name', 'Last Name': 'name',
                'Date of_Birth': 'date_of_birth', 'Gender': 'gender', 'Family ID': 'family_id',
                'Camp ID': 'camp_id', 'Triage Category': 'triage_category', 'Medical Conditions': 'medical_condition',
                'Vital Status': 'vital_status'}
        self.fields_to_be_dropdown = {'Camp ID': [camp.campID for camp in CampDataRetrieve.get_all_camps()], 'Vital Status': ['Alive', 'Deceased'], 
                                      'Gender': ['Male', 'Female', 'Other'], 'Triage Category': ['None', 'Non-Urgent', 'Standard', 'Urgent', 'Very-Urgent', 'Immediate']}
        self.button_labels = ['Save Changes', 'Delete']
        self.current_data = self.screen_data.display_info()
        self.save_record = PersonDataEdit.update_refugee
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditPersonalDetails(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Personal Details']
        self.modifiable_variables = ['Volunteer ID', 'First Name', 'Last Name', 'Username',
                'Date of Birth', 'Phone', 'Account Status', 'Camp ID']
        self.filter_matching = {'Volunteer ID': 'volunteerID', 'First Name': 'name', 'Last Name': 'name', 'Username': 'username',
                'Date of Birth': 'date_of_birth', 'Phone': 'phone', 'Camp ID': 'campID', 'Account Status': 'account_status'}
        self.button_labels = ['Save Changes']#, 'Delete', 'Deactivate']
        self.current_data = self.logged_in_user.display_info()
        self.save_record = PersonDataEdit.update_volunteer
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()
