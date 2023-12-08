import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ..Logic.plan_data_retrieve import PlanDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.person_data_retrieve import PersonDataRetrieve
import pandas as pd


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
        self.setup_list()

    def setup_list(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different lists")

    def update_results_list(self, filter, searchbar):
        
        


        # the following displays a dismissible pop up if the filter is not changed from default
        if filter == 'Filter':
            popup = tk.Toplevel(self.root)

            # Set the title of the popup window
            popup.title("Popup Window")

            # Add some content to the popup
            msg = tk.Label(popup, text="Please select a search filter")
            msg.pack(padx=20, pady=20)

            # Add a dismiss button
            dismiss_button = tk.Button(popup, text="Dismiss", command=popup.destroy)
            dismiss_button.pack(pady=10)
            return
        
        get_list_input = {self.filter_matching[filter]: searchbar}

        self.results_list.destroy()

        if searchbar == '':
            self.list_data = PlanDataRetrieve.get_plans()
            self.create_results()
            return

        # extracting the searched objects
        self.list_data = self.get_search(**get_list_input)

        # setting the internal results to the updated value

        self.create_results()

    def create_title(self):
        # this method creates the title and add entry button for each list
        # page_top_frame = tk.Frame(self.root)
        # page_top_frame.pack(side='top')

        list_title = ttk.Label(self, text=self.list_type[0], font=("Helvetica", 20, "bold"))
        list_title.grid(column=6, row=0, padx=10, pady=5)

        new_plan_button = ttk.Button(self, text=self.list_type[1], command=self.switch_to_new_plan)
        new_plan_button.grid(column=6, row=1, padx=10, pady=5)

    def create_search(self):
        # this creates the search bar, filters and search button
        # search_frame = tk.Frame(self.root)
        # search_frame.pack()

        search_filters = ttk.Combobox(self, values=self.list_headers, state="readonly")
        search_filters.set("Filter")  # set default value
        search_filters.grid(column=5, row=2, padx=5)
        # search_filters.bind('<<ComboboxSelected>>', )

        activity_status = ttk.Combobox(self, values=['All', 'Active', 'Ended'])
        activity_status.set("Status")
        activity_status.grid(column=4, row=2, padx=5)

        search_bar = ttk.Entry(self, width=100)
        search_bar.grid(column=6, row=2, padx=5)
        # search_bar.pack(padx=10, pady=5)

        search_button = ttk.Button(self, text='Search',
                                   command=lambda: self.update_results_list(search_filters.get(), search_bar.get()))
        search_button.grid(column=7, row=2)
        # search_button.pack(side='right', padx=10, pady=5)

        export_data_button = ttk.Button(self, text='Export Results', command=self.export_data)
        export_data_button.grid(column=8, row=2, padx=5)
        
    def create_results(self):
        # this method creates the results list for a chosen subclass
        self.results_list = ttk.Treeview(self, columns=self.list_headers, show='headings')

        # this lets us change the header values depending on what are being passed
        for i in self.list_headers:
            self.results_list.heading(i, text=i)
            self.results_list.column(i, anchor='center')

        # self.tree_item_to_object = {}

        # Insert items into the Treeview and populate the dictionary
        for result in self.list_data:
            result_id = self.results_list.insert('', 'end', values=result.display_info())
            self.tree_item_to_object[result_id] = result

        # print("Tree items to objects:", self.tree_item_to_object)

        # Bind double-click event
        self.results_list.bind('<Double-1>', lambda event: self.on_item_double_click(event))

        # Place the Treeview on the grid
        self.results_list.grid(column=0, row=3, columnspan=13)

        # print("Tree items to objects:", self.tree_item_to_object)

    def on_item_double_click(self, event):
        # Identify the Treeview widget
        tree = event.widget

        # Get the selected item
        result_id = tree.selection()[0]

        # print("Current tree_item_to_object dictionary:", self.tree_item_to_object)
        # print("Clicked item ID:", result_id)

        # Retrieve the associated object from the dictionary
        associated_object = self.tree_item_to_object[result_id]

        if associated_object:
            self.show_screen(self.switch_to_page, associated_object)
            #print(self.switch_to_page, associated_object)
        else:
            print("no asssociated object")

    def switch_to_new_plan(self, event=None):
        self.show_screen('NewPlan')


    def export_data(self):

        data_list = [object.display_info() for object in self.list_data]

        df = pd.DataFrame(data_list, columns=self.list_headers)
        
        #df.to_csv(self.export_name + '.csv', index=False)

        file_path = filedialog.asksaveasfilename(initialfile=self.export_name + '.csv',
                                             defaultextension=".csv", 
                                             filetypes=[("CSV files", "*.csv")])

        if file_path:  
            df.to_csv(file_path, index=False)

            


class PlanList(ManageList):
    def setup_list(self):
        self.list_type = ['Manage Plans', 'Add New Plan']
        self.list_headers = ['Plan ID', 'Plan Name', 'Country', 'Event Name', 'Description', 'Start Date', 'End Date']
        self.list_data = PlanDataRetrieve.get_plans()
        self.get_search = PlanDataRetrieve.get_plan
        self.switch_to_page = 'AdminDashboard'
        self.filter_matching = {'Plan ID': 'planID', 'Plan Name': 'name', 'Country': 'country', 'Event Name': 'event name',
                                'Description': 'description', 'Start Date': 'start date', 'End Date': 'end date'}
        self.export_name = 'Plans'
        self.create_title()
        self.create_search()
        self.create_results()


class CampList(ManageList):
    def setup_list(self):
        self.list_type = ['Manage Camps', 'Add New Camp']
        self.list_headers = ['Camp ID', 'Country', 'Max Shelter', 'Water', 'Max Water', 'Food', 'Max_Food',
                             'Medical Supplies', 'Max Medical Supplies', 'Plan ID']
        self.list_data = camp.get_camps()
        self.switch_to_page = 'EditCamp'
        self.filter_matching = {'Camp ID': 'campID', 'Country': 'location', 'Max Shelter': 'max_shelter', 'Water': 'water', 'Max Water': 'max_water', 'Food': 'food', 'Max_Food': 'max_food',
                                'Medical Supplies': 'medical_supplies', 'Max Medical Supplies': 'max_medical_supplies', 'Plan ID': 'planID'}
        self.create_title()
        self.create_search()
        self.create_results()


class VolunteerList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Volunteers', 'Add New Volunteer']
        self.list_headers = ['Plan ID', 'Plan Name', 'Plan Type', 'Country', 'Description', 'Start Date', 'End Date']
        self.list_data = None  # to be provided by logid layer
        self.switch_to_page = 'EditVolunteer'
        self.create_title()
        self.create_search()
        self.create_results()


class RefugeeList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Refugees', 'Add New Refugee']
        self.list_headers = ['Plan ID', 'Plan Name', 'Plan Type', 'Country', 'Description', 'Start Date', 'End Date']
        self.list_data = [['1', 'Austerity relief', 'economic collapse', 'United Kingdom',
                           'Aims to provide support to those suffering from cosy livs', '25/11/2023', 'next GE']]
        self.switch_to_page = 'EditRefugee'
        self.create_title()
        self.create_search()
        self.create_results()
