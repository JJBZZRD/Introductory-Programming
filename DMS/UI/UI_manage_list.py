import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ..Logic.plan_data_retrieve import PlanDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..DB.camp import Camp
from ..DB.plan import Plan
from ..Logic.audit_data_retrieve import AuditDataRetrieve
import pandas as pd

#this class generates a list page. variations are sest using the subclasses
class ManageList(tk.Frame):
    def __init__(self, ui_manager, **kwargs):
        super().__init__(ui_manager.root, **kwargs)
        self.root = ui_manager.root
        self.screen_data = ui_manager.screen_data
        self.show_screen = ui_manager.show_screen
        self.tree_item_to_object = {}
        self.results_list = None
        self.list_type = None
        self.list_headers = None
        self.list_data = None
        self.search_field = None
        self.switch_to_page = None
        self.get_search = None
        self.filter_matching = {}
        self.export_name = ''
        self.status_filters = []
        self.record_button = None
        self.filter_values = None
        self.setup_list()

    def setup_list(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different lists")

    def update_results_list(self, filter, searchbar, status=None, **kwargs):
        
        search_text = searchbar

        if searchbar == '':
            search_text = None

        # the following displays a dismissible pop up if the filter is not changed from default
        if filter == 'Filter' or status == 'Status':
            popup = tk.Toplevel(self.root)
            popup.title("Popup Window")

            msg = tk.Label(popup, text="Please select a search filter")
            msg.pack(padx=20, pady=20)

            dismiss_button = tk.Button(popup, text="Dismiss", command=popup.destroy)
            dismiss_button.pack(pady=10)
            return
        
        get_list_input = {self.filter_matching[filter]: search_text}

        self.results_list.destroy()

        status_filter = None

        if status:
            match status:
                case 'All':
                    pass
                case 'Active':
                    get_list_input.update({'active': True})
                
                case 'Ended':
                    get_list_input.update({'active': False})
                
                case 'Inactive':
                    get_list_input.update({'active': False})
                

        # extracting the searched objects
        self.list_data = self.get_search(**get_list_input)

        # setting the internal results to the updated value

        self.create_results()

    def create_title(self, plan=False):
        #this method creates the title and add entry button for each list


        list_title = ttk.Label(self, text=self.list_type[0], font=("Helvetica", 20, "bold"))
        list_title.grid(column=6, row=0, padx=10, pady=5)

        if len(self.list_type) > 1:
            new_plan_button = ttk.Button(self, text=self.list_type[1], command=self.new_record_button)
            new_plan_button.grid(column=6, row=1, padx=10, pady=5)

        if plan:
            manage_camps = ttk.Button(self, text='  Manage Camps   ', command=lambda page='CampList': self.show_screen(page))
            manage_camps.grid(column=4, row=0, padx=5, pady=5)
                                                      
            manage_volunteers = ttk.Button(self, text='Manage Volunteers', command=lambda page='VolunteerList': self.show_screen(page))
            manage_volunteers.grid(column=4, row=1, padx=5, pady=5)

            manage_refugees = ttk.Button(self, text=' Manage Refugees ', command=lambda page='RefugeeList': self.show_screen(page))
            manage_refugees.grid(column=4, row=2, padx=5, pady=5)

            audit_logs = ttk.Button(self, text='Audit Logs', command=lambda page='AuditLogs': self.show_screen(page))
            audit_logs.grid(column=8, row=0, padx=5, pady=5)

    def create_search(self):
        # this creates the search bar, filters and search button

        search_filters = ttk.Combobox(self, values=self.filter_values, state="readonly")
        search_filters.set("Filter")  
        search_filters.grid(column=5, row=3, padx=5)

        if self.status_filters:
            activity_status = ttk.Combobox(self, values=self.status_filters)
            activity_status.set("Status")
            activity_status.grid(column=4, row=3, padx=5)
            search_button = ttk.Button(self, text='Search',
                                   command=lambda: self.update_results_list(search_filters.get(), search_bar.get(), status=activity_status.get()))
        else:
            search_button = ttk.Button(self, text='Search',
                                   command=lambda: self.update_results_list(search_filters.get(), search_bar.get()))

        search_bar = ttk.Entry(self, width=100)
        search_bar.grid(column=6, row=3, padx=5)

        
        search_button.grid(column=7, row=3)

        export_data_button = ttk.Button(self, text='Export Results', command=self.export_data)
        export_data_button.grid(column=8, row=3, padx=5)
        
    def create_results(self):
        #this method create the results list for a chosen subclass
        self.results_list = ttk.Treeview(self, columns=self.list_headers, show='headings')

        #this lets us change the header values depending on what are being passed
        for i in self.list_headers:
            self.results_list.heading(i, text=i)
            self.results_list.column(i, anchor='center', width=int(1000/len(self.list_headers)))


        # Insert items into the Treeview and populate the dictionary
        for result in self.list_data:
            result_id = self.results_list.insert('', 'end', values=result.display_info())
            self.tree_item_to_object[result_id] = result


        
        self.results_list.bind('<Double-1>', lambda event: self.on_item_double_click(event))

        
        self.results_list.grid(column=0, row=4, columnspan=12, sticky='nsew')

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.results_list.yview)
        scrollbar.grid(column=12, row=4, sticky='ns')

        
        self.results_list.configure(yscrollcommand=scrollbar.set)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)


    def on_item_double_click(self, event):
        tree = event.widget

        result_id = tree.selection()[0]

        associated_object = self.tree_item_to_object[result_id]

        if associated_object:
            self.show_screen(self.switch_to_page, associated_object)
        else:
            print("no asssociated object")

    def new_record_button(self, event=None):
        self.show_screen(self.record_button)


    def export_data(self):

        data_list = [object.display_info() for object in self.list_data]

        df = pd.DataFrame(data_list, columns=self.list_headers)
        

        file_path = filedialog.asksaveasfilename(initialfile=self.export_name + '.csv',
                                             defaultextension=".csv", 
                                             filetypes=[("CSV files", "*.csv")])

        if file_path:  
            df.to_csv(file_path, index=False)



class PlanList(ManageList):
    def setup_list(self):
        self.list_type = ['Manage Plans', 'Add New Plan']
        self.list_headers = ['Plan ID', 'Plan Name', 'Country', 'Event Name', 'Description', 'Start Date', 'End Date', 'Water', 'Food', 'Medical Supplies', 'Shelter', 'Status', 'Creation Time']
        self.filter_values = ['Plan ID', 'Plan Name', 'Country', 'Event Name', 'Description', 'Start Date', 'End Date']
        self.list_data = PlanDataRetrieve.get_all_plans()
        self.get_search = PlanDataRetrieve.get_plan
        self.switch_to_page = 'AdminDashboard'
        self.record_button = 'NewPlan'
        self.filter_matching = {'Plan ID': 'planID', 'Plan Name': 'name', 'Country': 'country', 'Event Name': 'event_name',
                                'Description': 'description', 'Start Date': 'start_date', 'End Date': 'end_date', 'Status': 'active' ,'Creation Time': 'created_time', 'Water':'water', 'Food':'food', 'Medical Supplies':'medical_supplies', 'Shelter':'shelter'}
        self.status_filters = ['All', 'Active', 'Ended']
        self.export_name = 'Plans'
        self.create_title(plan=True)
        self.create_search()
        self.create_results()

    

class CampList(ManageList):
    def setup_list(self):
        self.list_type = ['Manage Camps', 'Add New Camp']
        self.list_headers = ['Camp ID', 'Name', 'Shelter', 'Water', 'Food', 'Medical Supplies', 'Plan ID', 'Creation Time']
        self.filter_values = ['Camp ID', 'Name', 'Shelter', 'Water', 'Food', 'Medical Supplies', 'Plan ID']
        self.list_data = self.list_by_plan()
        self.get_search = CampDataRetrieve.get_camp
        self.switch_to_page = 'EditCamp'
        self.record_button = 'NewCamp'
        self.filter_matching = {'Camp ID': 'campID', 'Name': 'location', 'Shelter': 'shelter', 'Water': 'water', 
                                'Food': 'food', 'Medical Supplies': 'medical_supplies', 'Plan ID': 'planID', 'Creation Time': 'created_time' }
        self.export_name = 'Camps'
        self.modify_title()
        self.create_title()
        self.create_search()
        self.create_results()


    def list_by_plan(self):
        if isinstance(self.screen_data, Plan):
            return CampDataRetrieve.get_camp(planID=self.screen_data.planID)
        else:
            return CampDataRetrieve.get_all_camps()

    def modify_title(self):
        if isinstance(self.screen_data, Plan):
            self.list_type[0] = f'Manage Camps for Plan {self.screen_data.planID}'
        else:
            self.list_type[0] = f'Manage camps: Global'

class VolunteerList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Volunteers', 'Add New Volunteer']
        self.list_headers = ['Volunteer ID', 'First Name', 'Last Name', 'Username',
                'Date of Birth', 'Phone', 'Account Status', 'Camp ID', 'Creation Time']
        self.filter_values = ['Volunteer ID', 'Name', 'Username',
                'Date of Birth', 'Phone', 'Camp ID']
        self.list_data = self.list_by_plan()
        self.get_search = PersonDataRetrieve.get_volunteers
        self.switch_to_page = 'EditVolunteer'
        self.record_button = 'NewVolunteer'
        self.filter_matching = {'Volunteer ID': 'volunteerID', 'Name': 'name', 'Last Name': 'name', 'Username': 'username',
                'Date of Birth': 'date_of_birth', 'Phone': 'phone', 'Camp ID': 'campID', 'Creation Time': 'created_time'}
        self.status_filters = ['All', 'Active', 'Inactive']
        self.modify_title()
        self.create_title()
        self.create_search()
        self.create_results()


    def list_by_plan(self):
        #this method provides a list of volunteers for a specific plan if a camp is provided
        if isinstance(self.screen_data, Camp):
            planID = self.screen_data.planID

            camps_under_plan = CampDataRetrieve.get_camp(planID=planID)

            camp_id_under_plan = [camp.campID for camp in camps_under_plan]

            volunteers_of_camps = []

            for camp_id in camp_id_under_plan:
                volunteers_of_camps += PersonDataRetrieve.get_volunteers(campID=camp_id)

            return volunteers_of_camps
        else:
            return PersonDataRetrieve.get_all_volunteers()
        
    def modify_title(self):
        if isinstance(self.screen_data, Camp):
            self.list_type[0] = f'Manage Volunteers for Plan {self.screen_data.planID}'
        else:
            self.list_type[0] = f'Manage Vounteers: Global'


class RefugeeList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Refugees', 'Add New Refugee']
        self.list_headers = ['Refugee ID', 'First Name', 'Last Name',
                'Date of Birth', 'Gender', 'Family ID',
                'Camp ID', 'Triage Category', 'Medical Conditions',
                'Vital Status', 'Creation Time']
        self.filter_values = ['Plan ID', 'Refugee ID', 'Name',
                'Date of Birth', 'Gender', 'Family ID',
                'Camp ID', 'Triage Category', 'Medical Conditions',
                'Vital Status']
        self.list_data = self.list_by_camp()
        self.get_search = PersonDataRetrieve.get_refugees
        self.switch_to_page = 'EditRefugee'
        self.record_button = 'NewRefugee'
        self.filter_matching = {'Refugee ID': 'id', 'Name': 'name', 'Last Name': 'name',
                'Date of Birth': 'date_of_birth', 'Gender': 'gender', 'Family ID': 'family_id',
                'Camp ID': 'camp_id', 'Triage Category': 'triage_category', 'Medical Conditions': 'medical_condition',
                'Vital Status': 'vital_status','Creation Time': 'created_time', 'Plan ID':'planID'}
        self.export_name = 'Refugees'
        self.modify_title()
        self.create_title()
        self.create_search()
        self.create_results()

    def list_by_camp(self):
        if isinstance(self.screen_data, Camp):
            return PersonDataRetrieve.get_refugees(camp_id=self.screen_data.campID)
        else:
            return PersonDataRetrieve.get_all_refugees()
    
    def modify_title(self):
        if isinstance(self.screen_data, Camp):
            self.list_type[0] = f'Manage Refugees for Camp {self.screen_data.campID}'
        else:
            self.list_type[0] = f'Manage Refugees: Global'

class AuditLogs(ManageList):

    def setup_list(self):
        self.list_type = ['Audit Logs']
        self.list_headers = ['Log ID', 'Table Name', 'Record ID', 'Field Name', 'Old Value', 'New Value', 'Action', 'Created Time', 'Changed By']
        self.filter_values = ['Table Name', 'Record ID', 'Field Name', 'Old Value', 'New Value', 'Action', 'Changed By']
        self.list_data = AuditDataRetrieve.get_all_audit_logs()
        self.get_search = AuditDataRetrieve.get_audit_logs
        self.filter_matching ={'Table Name': 'table_name', 'Record ID': 'recordID', 'Field Name': 'field_name', 'Old Value': 'old_value', 'New Value': 'new_value', 'Action': 'action', 'Changed By': 'changed_by'}
        self.export_name = 'Audit Logs'
        self.create_title()
        self.create_search()
        self.create_results()