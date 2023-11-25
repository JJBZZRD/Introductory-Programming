import tkinter as tk
from tkinter import ttk
from UI_dashboard import AdminDashboard
from UI_modify_entries import NewPlan


class ManageList(tk.Frame):
    def __init__(self, root, show_screen, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.show_screen = show_screen
        self.setup_list()
        self.list_type = None
        self.result_headers = None
        self.results = None
        self.search_field = None

    def setup_list(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different lists")

    def result_list(self):
        # need to gather the search bar value. there needs to be a backend update to gather the
        # associated results from the search. this will have to be in array value.
        # the collected results will be assigned to the self.results value.
        # the create_result will then be recalled to display the new list
        pass

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

        search_filters = ttk.Combobox(self, values=self.result_headers, state="readonly")
        search_filters.set("Filter")  # set default value
        search_filters.grid(column=5, row=2, padx=5)
        # search_filters.bind('<<ComboboxSelected>>', )

        search_bar = ttk.Entry(self, width=100)
        search_bar.grid(column=6, row=2, padx=5)
        self.search_field = search_bar.get()
        # search_bar.pack(padx=10, pady=5)

        search_button = ttk.Button(self, text='Search', command=self.result_list)
        search_button.grid(column=7, row=2)
        # search_button.pack(side='right', padx=10, pady=5)

        # we need a list of lists to represent the data to occupy the results list.
        # then each list within thi list will populate the row from the treeview widget under the appropriate header

    def create_results(self):
        #this method creates the results list for a chosen subclass
        results_list = ttk.Treeview(self, columns=self.result_headers, show='headings')

        # this lets us change the header values depending on what are being passed
        for i in self.result_headers:
            results_list.heading(i, text=i)
            results_list.column(i, anchor='center')

        for i in self.results:
            results_list.insert('', 'end', values=i)

        results_list.bind('<Double-1>', self.switch_to_admin_dashboard)

        results_list.grid(column=0, row=3, columnspan=13)

    def switch_to_admin_dashboard(self, event=None):
        self.show_screen(AdminDashboard)
        self.destroy()

    def switch_to_new_plan(self, event=None):
        self.show_screen(NewPlan)
        self.destroy()


class PlanList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Plans', 'Add New Plan']
        self.result_headers = ['Plan ID', 'Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date']
        self.results = [['1', 'Austerity relief', 'economic collapse', 'United Kingdom',
                         'Aims to provide support to those suffering from cosy livs', '25/11/2023', 'next GE']]
        self.create_title()
        self.create_search()
        self.create_results()


class VolunteerList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Volunteers', 'Add New Volunteer']
        self.result_headers = ['Plan ID', 'Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date']
        self.results = [['1', 'Austerity relief', 'economic collapse', 'United Kingdom',
                         'Aims to provide support to those suffering from cosy livs', '25/11/2023', 'next GE']]
        self.create_title()
        self.create_search()


class RefugeeList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Refugees', 'Add New Refugee']
        self.result_headers = ['Plan ID', 'Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date']
        self.results = [['1', 'Austerity relief', 'economic collapse', 'United Kingdom',
                         'Aims to provide support to those suffering from cosy livs', '25/11/2023', 'next GE']]
        self.create_title()
        self.create_search()
