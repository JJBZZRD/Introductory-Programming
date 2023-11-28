import tkinter as tk
from tkinter import ttk
from dummydata import Camp, camp1
from dummydata import Refugee, refugee1, refugee2


class Dashboard(tk.Frame):
    def __init__(self, root, show_screen, *args, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.setup_dashboard(*args)
        self.show_screen = show_screen

    def setup_dashboard(self):
        raise NotImplementedError("Subclasses should implement this method to setup the dashboard layout")
    
    
    def populate_camp_tab(self, tab, camp):
        print(f"Populating tab for Camp ID: {camp.campID}")  # Debug print

        # Split the frame into left and right sections
        left_frame = tk.Frame(tab, bg='white')
        right_frame = tk.Frame(tab, bg='white')
        left_frame.pack(side='left', fill='both', expand=True)
        right_frame.pack(side='right', fill='both', expand=True)

        # Create resources section in left frame
        resources = {
            'Water': (camp.water, camp.max_water),
            'Food': (camp.food, camp.max_food),
            'Medical Supplies': (camp.medical_supplies, camp.max_medical_supplies)
        }

        for resource_name, (amount, capacity) in resources.items():
            self.create_resource_frame(left_frame, resource_name, amount, capacity, f"Camp {camp.campID}")

        ttk.Button(left_frame, text="Edit Camp", command=lambda: self.show_screen('EditCamp', camp.campID)).pack(pady=5)

        # Create refugees section in right frame
        self.create_refugees_section(right_frame, camp)

    def create_refugees_section(self, parent, camp):
        # Title for the refugees section
        # refugees = logic.getrefugees(camp, camp.campID)

        refugees = [refugee1, refugee2]#placeholder

        refugees_title = tk.Label(parent, text=f"Refugees in Camp {camp.campID}", font=('Arial', 16, 'bold'))
        refugees_title.pack(pady=10)

        # Search and filter frame (placeholders for future functionality)
        search_frame = tk.Frame(parent, bg='white')
        search_frame.pack(pady=5, fill='x')
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side='left', padx=5, expand=True, fill='x')
        filter_button = ttk.Button(search_frame, text="Filter")
        filter_button.pack(side='left', padx=5)
        search_button = ttk.Button(search_frame, text="Search")
        search_button.pack(side='left', padx=5)

        # Dynamically display refugee list
        refugees_listbox = tk.Listbox(parent)
        for refugee in refugees:
            refugees_listbox.insert(tk.END, f"{refugee.first_name} {refugee.last_name} - {refugee.medical_condition}")
        refugees_listbox.pack(pady=10, expand=True, fill='both')

        # Manage refugees button (placeholder)
        manage_refugees_button = ttk.Button(parent, text="Manage Refugees", command=lambda: self.show_screen('RefugeeList'))
        manage_refugees_button.pack(pady=5)


    def create_resource_frame(self, parent, resource_name, amount, capacity, camp=None):
        resource_frame = tk.Frame(parent)
        resource_frame.pack(fill='x', expand=True)

        tk.Label(resource_frame, text=f"{resource_name}:").pack(side='left')
        amount_label = tk.Label(resource_frame, text=f"{amount}/{capacity}")
        amount_label.pack(side='left')

        ttk.Button(resource_frame, text="-", width=2, command=lambda: self.adjust_resource(camp.campID, resource_name, -1, amount_label)).pack(side='left')
        ttk.Button(resource_frame, text="+", width=2, command=lambda: self.adjust_resource(camp.campID, resource_name, 1, amount_label)).pack(side='left')

    def adjust_resource(self, adjustment):
        new_amount = self.amount + adjustment
        if 0 <= new_amount <= self.capacity:
            self.amount = new_amount
            self.amount_label.config(text=f"{self.amount}/{self.capacity}")
            if self.adjust_callback:
                self.adjust_callback(self.resource_name, new_amount)


class VolunteerDashboard(Dashboard):
    def setup_dashboard(self, userID):
        # Assuming logic.getvolunteer and logic.getcamp are placeholders
        # VolunteerUser = logic.getvolunteer(id, user_id)  
        # VolunteerCamp = logic.getcamp(id, VolunteerUser.campid)
        # Directly using camp1 for this example
        self.create_volunteer_tab(camp1)


    def create_volunteer_tab(self,camp):
        print(f"Creating tab for Camp ID: {camp.campID}")
        self.tab_control = ttk.Notebook(self)
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=f'Camp {camp.campID}')
        self.populate_camp_tab(tab, camp)
        self.tab_control.pack(expand=1, fill="both")


class AdminDashboard(Dashboard):
    def setup_dashboard(self):
        # camps = get_plan_camps()
        # for camp in camps
            # create tabs
        
        self.create_admin_tabs()
    
    def create_admin_tabs(self):
        self.tab_control = ttk.Notebook(self)
        self.overview_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text='Overview')
        self.populate_overview_tab(self.overview_tab)
        for i in range(1, 4):
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=f'Camp {i}')
            self.populate_camp_tab(tab, i)
        self.tab_control.pack(expand=1, fill="both")

    def populate_overview_tab(self, tab):
        # Sample data for camps and resources
        camps_data = {
            'Camp 1': {'Tents': [80, 100], 'Food': [60, 80], 'Water': [50, 70], 'Medicine': [30, 50]},
            'Camp 2': {'Tents': [40, 60], 'Food': [90, 120], 'Water': [70, 90], 'Medicine': [20, 40]},
            'Camp 3': {'Tents': [50, 80], 'Food': [30, 60], 'Water': [80, 100], 'Medicine': [60, 80]}
        }

        # Additional resources
        additional_resources = {'Tents': [20, 50], 'Food': [40, 100], 'Water': [30, 80], 'Medicine': [10, 60]}

        camps_frame = tk.Frame(tab)
        camps_frame.pack(side='left', fill='both', expand=True)

        for camp_name, resources in camps_data.items():
            camp_frame = tk.Frame(camps_frame, borderwidth=1, relief='solid')
            camp_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            tk.Label(camp_frame, text=camp_name, font=('Arial', 16, 'bold')).pack(pady=(5, 10))

            for resource_name, (amount, capacity) in resources.items():
                self.create_resource_frame(camp_frame, resource_name, amount, capacity, camp_name)

            ttk.Button(camp_frame, text="Edit Camp", command=lambda cn=camp_name: self.show_screen('EditCamp', cn)).pack(pady=5)

        additional_resources_frame = tk.Frame(tab, bg='lightgray', bd=2, relief='groove')
        additional_resources_frame.pack(side='right', fill='y', padx=(5, 0))
        tk.Label(additional_resources_frame, text="Additional Resources Available", bg='lightgray').pack(pady=10)
    
        for resource_name, (amount, capacity) in additional_resources.items():
            self.create_resource_frame(additional_resources_frame, resource_name, amount, capacity)