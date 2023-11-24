import tkinter as tk
from tkinter import ttk
from UI_dashboard import AdminDashboard


class ManageList(tk.Frame):
    def __init__(self, root, show_screen, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.show_screen = show_screen
        self.setup_list()
        self.list_type = None
        self.result_headers = None
        self.results = None

    def setup_list(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different lists")

    def create_title(self):
        page_top_frame = tk.Frame(self.root)
        page_top_frame.pack(side='top')

        list_title = ttk.Label(page_top_frame, text=self.list_type[0], font=("Helvetica", 20, "bold"))
        list_title.pack(padx=10, pady=5)

        new_plan_button = ttk.Button(page_top_frame, text=self.list_type[1])
        new_plan_button.pack(padx=10, pady=5)

    def result_list(self):
        # need to gather the search bar value. there needs to be a backend update to gather the
        # associated results from the search. this will have to be in array value.
        # the collected results will be assigned to the self.results value.
        # the create_search frame can then be recalled (certain states will be lost like the filter selection)
        pass

    def create_search(self):
        search_frame = tk.Frame(self.root)
        search_frame.pack()

        search_filters = ttk.Combobox(search_frame, values=self.result_headers, state="readonly")
        search_filters.set("Filter")  # set default value
        search_filters.grid(column=5, row=0, padx=5)
        # search_filters.bind('<<ComboboxSelected>>', )

        search_bar = ttk.Entry(search_frame, width=100)
        search_bar.grid(column=6, row=0, padx=5)
        # search_bar.pack(padx=10, pady=5)

        search_button = ttk.Button(search_frame, text='Search', command=self.result_list)
        search_button.grid(column=7, row=0)
        # search_button.pack(side='right', padx=10, pady=5)

        results_list = ttk.Treeview(search_frame, columns=self.result_headers, show='headings')

        # this lets us change the header values depending on what are being passed
        for i in self.result_headers:
            results_list.heading(i, text=i)
            results_list.column(i, anchor='center')

        for i in self.results:
            results_list.insert('', 'end', values=i)

        results_list.bind('<Double-1>', self.switch_screen)

        results_list.grid(column=0, row=1, columnspan=13)
        # we need a list of lists to represent the data to occupy the results list.
        # then each list within thi list will populate the row from the treeview widget under the appropriate header

    def switch_screen(self, event=None):
        self.pack_forget()
        self.show_screen(AdminDashboard)



class PlanList(ManageList):

    def setup_list(self):
        self.list_type = ['Manage Plans', 'Add New Plan']
        self.result_headers = ['Plan ID', 'Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date']
        self.results = [['1', 'Austerity relief', 'economic collapse', 'United Kingdom',
                         'Aims to provide support to those suffering from cosy livs', '25/11/2023', 'next GE']]
        self.create_title()
        self.create_search()
