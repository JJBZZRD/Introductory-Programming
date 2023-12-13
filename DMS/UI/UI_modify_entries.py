import tkinter as tk
from tkinter import ttk
from ..Logic.camp_data_edit import CampDataEdit
from ..Logic.plan_data_edit import PlanEdit
from ..Logic.person_data_edit import PersonDataEdit
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.plan_data_retrieve import PlanDataRetrieve
from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..DB.countries import get_all_countries
from ..DB.camp import Camp
from ..DB.plan import Plan

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
        self.screen_data_id = None
        self.page_nav_on_delete = None
        self.passed_id = {}
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
            if variable in self.fields_to_be_dropdown and variable not in self.passed_id:
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
                
                if variable in self.passed_id:
                    placeholder = self.passed_id[variable]

                elif self.current_data is not None and i < len(self.current_data):
                    placeholder = self.current_data[i]
                elif "Date" in variable:
                    placeholder = "yyyy-mm-dd"
                elif variable in ["Water", "Food", "Medical Supplies", "Shelter"]:
                    placeholder = "0"
                else:
                    placeholder = "Enter " + variable


                entry_field.insert(0, placeholder)
                entry_field.bind("<FocusIn>", lambda event, e=entry_field, p=placeholder: self.on_focus_in(event, e, p))
                entry_field.bind("<FocusOut>", lambda event, e=entry_field, p=placeholder: self.on_focus_out(event, e, p))

                if variable in self.read_only_fields:
                    entry_field['state'] = 'readonly'

                if variable == 'Password':
                    entry_field.config(show="*")
    
            

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
                #print(inputs)
                #print(tuple(inputs))

                
                print(f"inputs: {inputs}")  
                self.ui_error_popup(self.save_record(**inputs, logged_in_user=self.logged_in_user))
                # try to update data using the business logic function

            case 'Delete':

                # logic for deleting object passed into screen data

                self.confirmation_popup('Are you sure you want to delete?', self.delete_record)

                
            case 'Deactivate':

                # logic for deactivating volunteer account
                pass
            case 'Create':
                inputs = {}
                for key in self.entry_fields:
                    inputs.update({self.entry_fields[key][0]: self.entry_fields[key][1].get()})
                #print(tuple(inputs))

                self.ui_error_popup(self.create_record(**inputs, logged_in_user=self.logged_in_user))
                #self.page_nav('back')

                pass
            case 'End':
                self.confirmation_popup('Are you sure you want to end this plan?', self.end_plan)


        # takes the entry field values




        # if returns true 
        # return success message utility

        # if returns list
        # return error message utility with error list as input?

    def ui_error_popup(self, function_result):
        if isinstance(function_result, str):
            popup = tk.Toplevel(self.root)
            popup.title("Error Window")

            msg = tk.Label(popup, text=function_result)
            msg.pack(padx=20, pady=20)

            dismiss_button = tk.Button(popup, text="Dismiss", command=popup.destroy)
            dismiss_button.pack(pady=10)
        else:
            popup = tk.Toplevel(self.root)
            popup.title("System Message")

            msg = tk.Label(popup, text="Operation Successful \n\n You can now close this window and navigage to other pages")
            msg.pack(padx=20, pady=20)

            dismiss_button = tk.Button(popup, text="Dismiss", command=lambda : (popup.destroy(), self.page_nav('back')))
            dismiss_button.pack(pady=10) 

    def confirmation_popup(self, text, function):
            popup = tk.Toplevel(self.root)
            popup.title("confirmation Window")

            msg = tk.Label(popup, text=text)
            msg.pack(padx=20, pady=20)

            dismiss_button = tk.Button(popup, text="Yes", command=lambda sdid = self.screen_data_id: (function(sdid), popup.destroy(), self.navigate_on_delete()))
            dismiss_button.pack(pady=10)

            dismiss_button = tk.Button(popup, text="No", command=popup.destroy)
            dismiss_button.pack(pady=10)
    
    def navigate_on_delete(self):
        if self.page_nav_on_delete:
            self.show_screen(*self.page_nav_on_delete)
        else:
            self.page_nav('back')

class NewPlan(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Plan']
        self.modifiable_variables = ['Plan Name', 'Event Name', 'Country', 'Description', 'Start Date', 'End Date', 'Water', 'Food', 'Medical Supplies', 'Shelter']
        self.filter_matching = {'Plan ID': 'planID', 'Plan Name': 'name', 'Country': 'country', 'Event Name': 'event_name',
                                'Description': 'description', 'Start Date': 'start_date', 'End Date': 'end_date', 'Water': 'water', 'Food': 'food', 'Medical Supplies': 'medical_supplies', 'Shelter': 'shelter', 'Status':'status'}
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
        self.modify_type = ['View/Edit Plan']
        self.modifiable_variables = ['Plan ID', 'Plan Name', 'Country', 'Event Name', 'Description', 'Start Date', 'End Date', 'Water', 'Food', 'Medical Supplies', 'Shelter', 'Status', 'Creation Time']
        self.filter_matching = {'Plan ID': 'planID', 'Plan Name': 'name', 'Country': 'country', 'Event Name': 'event_name',
                                'Description': 'description', 'Start Date': 'start_date', 'End Date': 'end_date', 'Water': 'water', 'Food': 'food', 'Medical Supplies': 'medical_supplies', 'Shelter': 'shelter', 'Status':'status', 'Creation Time': 'created_time'}
        self.button_labels = ['Save Changes', 'Delete', 'End']
        self.current_data = self.screen_data.display_info()
        self.save_record = PlanEdit.update_plan
        self.delete_record = PlanEdit.delete_plan
        self.page_nav_on_delete = ('PlanList', None)
        self.end_plan = PlanEdit.end_plan
        self.screen_data_id = self.screen_data.planID
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Country': get_all_countries()}
        self.read_only_fields = ['Plan ID', 'Creation Time', 'Status']
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class NewCamp(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Camp']
        self.modifiable_variables = ['Location', 'Shelter', 'Water', 'Food', 'Medical Supplies', 'Plan ID']
        self.filter_matching = {'Camp ID': 'campID', 'Location': 'location', 'Shelter': 'shelter', 'Water': 'water', 'Food': 'food', 'Medical Supplies': 'medical_supplies', 'Plan ID': 'planID'}
        self.button_labels = ['Create']
        self.create_record = CampDataEdit.create_camp
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Country': get_all_countries(), 'Plan ID': [plan.planID for plan in PlanDataRetrieve.get_all_plans()]}
        self.read_only_fields = []
        self.passed_id = self.plan_id_set()
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()

    def plan_id_set(self):
        #need to pass a plan id to the new camp if visited from dashboard and set to read only

        if isinstance(self.screen_data, Plan):
            planID = self.screen_data.planID

            self.read_only_fields.append('Plan ID')

            return {'Plan ID':planID}
        else:
            return {}


class EditCamp(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Camp']
        self.modifiable_variables = ['Camp ID', 'Location', 'Shelter', 'Water', 'Food', 'Medical Supplies', 'Plan ID', 'Creation Time']
        self.filter_matching = {'Camp ID': 'campID', 'Location': 'location', 'Shelter': 'shelter', 'Water': 'water', 'Food': 'food', 'Medical Supplies': 'medical_supplies', 'Plan ID': 'planID', 'Creation Time': 'created_time'}
        self.current_data = self.screen_data.display_info()
        self.button_labels = ['Save Changes', 'Delete']
        self.save_record = CampDataEdit.update_camp
        self.delete_record = CampDataEdit.delete_camp
        self.page_nav_on_delete = ('AdminDashboard', PlanDataRetrieve.get_plan(planID=self.screen_data.planID)[0])
        self.screen_data_id = self.screen_data.campID
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Plan ID': [plan.planID for plan in PlanDataRetrieve.get_all_plans()]}
        self.read_only_fields = ['Camp ID']
        self.if_logged_in_as_volunteer()
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()

    def if_logged_in_as_volunteer(self):
        if self.logged_in_user.volunteerID != 1:
            self.fields_to_be_dropdown = {}
            self.read_only_fields = ['Camp ID', 'Plan ID', 'Creation Time']
        else:
           self.fields_to_be_dropdown = {'Plan ID': [plan.planID for plan in PlanDataRetrieve.get_all_plans()]}
           self.read_only_fields = ['Camp ID', 'Creation Time']




class NewVolunteer(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Volunteer']
        self.modifiable_variables = ['First Name', 'Last Name', 'Username', 'Password',
                'Date of Birth', 'Phone', 'Account Status', 'Camp ID']
        self.filter_matching = {'Volunteer ID': 'volunteerID', 'First Name': 'first_name', 'Last Name': 'last_name', 'Username': 'username', 'Password': 'password',
                'Date of Birth': 'date_of_birth', 'Phone': 'phone', 'Camp ID': 'campID', 'Account Status': 'account_status'}
        self.button_labels = ['Create']
        # self.display_delete_button = False
        self.create_record = PersonDataEdit.create_volunteer
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Camp ID': [camp.campID for camp in CampDataRetrieve.get_all_camps()], 'Account Status': ['Active', 'Inactive']}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditVolunteer(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Volunteer']
        self.modifiable_variables = ['Volunteer ID', 'First Name', 'Last Name', 'Username',
                'Date of Birth', 'Phone', 'Account Status', 'Camp ID', 'Creation Time']
        self.filter_matching = {'Volunteer ID': 'volunteerID', 'First Name': 'first_name', 'Last Name': 'last_name', 'Username': 'username',
                'Date of Birth': 'date_of_birth', 'Phone': 'phone', 'Camp ID': 'campID', 'Account Status': 'account_status', 'Creation Time': 'created_time'}
        self.button_labels = ['Save Changes', 'Delete']
        self.current_data = self.screen_data.display_info()
        self.save_record = PersonDataEdit.update_volunteer
        self.delete_record = PersonDataEdit.delete_volunteer
        self.screen_data_id = self.screen_data.volunteerID
        self.entry_fields = {}
        self.fields_to_be_dropdown = {'Camp ID': [camp.campID for camp in CampDataRetrieve.get_all_camps()], 'Account Status': ['Active', 'Inactive']}
        self.read_only_fields = ['Volunteer ID', 'Creation Time']
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()
        # print(self.entry_fields)


class NewRefugee(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Refugee']
        self.modifiable_variables = ['First Name', 'Last Name',
                'Date of Birth', 'Gender', 'Family ID',
                'Camp ID', 'Triage Category', 'Medical Conditions',
                'Vital Status']
        self.filter_matching = {'First Name': 'first_name', 'Last Name': 'last_name',
                'Date of Birth': 'date_of_birth', 'Gender': 'gender', 'Family ID': 'family_id',
                'Camp ID': 'campID', 'Triage Category': 'triage_category', 'Medical Conditions': 'medical_conditions',
                'Vital Status': 'vital_status'}
        self.fields_to_be_dropdown = {'Camp ID': [camp.campID for camp in CampDataRetrieve.get_all_camps()], 'Vital Status': ['Alive', 'Deceased'], 
                                      'Gender': ['Male', 'Female', 'Other'], 'Triage Category': ['None', 'Non-Urgent', 'Standard', 'Urgent', 'Very-Urgent', 'Immediate']}
        self.button_labels = ['Create']
        self.create_record = PersonDataEdit.create_refugee
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditRefugee(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['View/Edit Refugee']
        self.modifiable_variables = ['Refugee ID', 'First Name', 'Last Name',
                'Date of Birth', 'Gender', 'Family ID',
                'Camp ID', 'Triage Category', 'Medical Conditions',
                'Vital Status', 'Creation Time']
        self.filter_matching = {'Refugee ID': 'id', 'First Name': 'first_name', 'Last Name': 'last_name', 'Date of Birth': 'date_of_birth', 'Gender': 'gender', 'Family ID': 'family_id',
                'Camp ID': 'campID', 'Triage Category': 'triage_category', 'Medical Conditions': 'medical_conditions',
                'Vital Status': 'vital_status', 'Creation Time': 'created_time'}
        self.fields_to_be_dropdown = {'Vital Status': ['Alive', 'Deceased'], 
                                      'Gender': ['Male', 'Female', 'Other'], 'Triage Category': ['None', 'Non-Urgent', 'Standard', 'Urgent', 'Very-Urgent', 'Immediate']}
        self.button_labels = ['Save Changes', 'Delete']
        self.current_data = self.screen_data.display_info()
        self.save_record = PersonDataEdit.update_refugee
        self.delete_record = PersonDataEdit.delete_refugee
        self.screen_data_id = self.screen_data.refugeeID
        self.entry_fields = {}
        self.read_only_fields = ['Refugee ID', 'Creation Time']
        self.campID_dropdown_values()
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()

    def campID_dropdown_values(self):
        refugee_campID = self.screen_data.campID

        camp_of_campID = CampDataRetrieve.get_camp(campID=refugee_campID)[0]

        planID_of_camp = camp_of_campID.planID

        camps = CampDataRetrieve.get_camp(planID=planID_of_camp)

        list_of_camp_ids = [camp.campID for camp in camps]

        self.fields_to_be_dropdown.update({'Camp ID': list_of_camp_ids})


class EditPersonalDetails(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Personal Details']
        self.modifiable_variables = ['Volunteer ID', 'First Name', 'Last Name', 'Username',
                'Date of Birth', 'Phone', 'Account Status', 'Camp ID', 'Creation Time', 'Password']
        self.filter_matching = {'Volunteer ID': 'volunteerID', 'First Name': 'first_name', 'Last Name': 'last_name', 'Username': 'username', 'Password': 'password',
                'Date of Birth': 'date_of_birth', 'Phone': 'phone', 'Camp ID': 'campID', 'Account Status': 'account_status', 'Creation Time': 'created_time'}
        self.button_labels = ['Save Changes']#, 'Delete', 'Deactivate']
        self.current_data = self.logged_in_user.display_info()
        self.save_record = PersonDataEdit.update_volunteer
        self.entry_fields = {}
        self.read_only_fields = ['Volunteer ID', 'Camp ID', 'Account Status', 'Creation Time']
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()

    def admin_user(self):
        if self.logged_in_user.camp_id is not None:
            self.read_only_fields.append('Camp ID')
