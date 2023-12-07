import tkinter as tk
from tkinter import ttk

from .UI_utlities import create_filterable_treeview 
from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.plan_data_retrieve import PlanDataRetrieve

class Dashboard(tk.Frame):
    def __init__(self, ui_manager, *args):
        super().__init__(ui_manager.root)
        self.root = ui_manager.root
        self.setup_dashboard(ui_manager.screen_data)
        self.show_screen = ui_manager.show_screen

    def setup_dashboard(self, *args):
        raise NotImplementedError("Subclasses should implement this method to setup the dashboard layout")
    
    
    def populate_camp_tab(self, tab, camp):
        print(f"Populating tab for Camp ID: {camp.campID}")

        left_frame = tk.Frame(tab, bg='white')
        right_frame = tk.Frame(tab, bg='white')
        left_frame.pack(side='left', fill='both', expand=True)
        right_frame.pack(side='right', fill='both', expand=True)

        self.create_resource_frame(left_frame, camp)

        ttk.Button(left_frame, text="Edit Camp", command=lambda: self.show_screen('EditCamp', camp)).pack(pady=5)

        self.create_refugees_section(right_frame, camp)

    import tkinter.ttk as ttk

    def create_refugees_section(self, parent, camp):
        refugees_title = tk.Label(parent, text=f"Refugees in Camp {camp.campID}", font=('Arial', 16, 'bold'))
        refugees_title.pack(pady=10)
        
        search_frame = tk.Frame(parent, bg='white')
        search_frame.pack(pady=5, fill='x')
        
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side='left', padx=5, expand=True, fill='x')
        search_entry.insert(0, camp.campID)

        filter_button = ttk.Button(search_frame, text="Filter/Search", command=lambda: self.update_refugees_list(search_entry, refugees_treeview))
        filter_button.pack(side='left', padx=5)

        refugees_treeview = ttk.Treeview(parent, columns=("Name", "Medical Condition"))
        refugees_treeview.pack(pady=10, expand=True, fill='both')
        refugees_treeview.bind('<Double-1>', lambda event, tv=refugees_treeview: self.on_refugee_double_click(event, tv))

        refugees_treeview.heading("#0", text="ID")
        refugees_treeview.column("#0", width=150, anchor='center')
        refugees_treeview.heading("Name", text="Name")
        refugees_treeview.column("Name", width=150)
        refugees_treeview.heading("Medical Condition", text="Medical Condition")
        refugees_treeview.column("Medical Condition", width=150)

        self.update_refugees_list(search_entry, refugees_treeview) 

    def update_refugees_list(self, search_entry, refugees_treeview):
        filter_value = search_entry.get().strip()
        filter_type = 'camp' if not filter_value else 'name'

        if not filter_value:
            filter_value = ''

        self.refugees = PersonDataRetrieve.get_refugees(filter_type, filter_value)

        if isinstance(self.refugees, str):
            print(self.refugees)
        else:
            refugees_treeview.delete(*refugees_treeview.get_children())
            if not self.refugees:
                refugees_treeview.insert("", "end", text="No matching refugees found.")
            else:
                for refugee in self.refugees:
                    print(refugee.__dict__) 
                    refugees_treeview.insert("", "end", text=refugee.refugeeID, values=(f"{refugee.first_name} {refugee.last_name}", refugee.medical_condition))
    
    def on_refugee_double_click(self, event, treeview):
        item = treeview.focus()
        if item:
            selected_refugee = self.refugees[int(treeview.item(item, "text")) - 1]
            self.show_screen('EditRefugee', selected_refugee)
        
    def create_resource_frame(self, parent, camp):
            resources = {
                'Water': (camp.water, camp.max_water),
                'Food': (camp.food, camp.max_food),
                'Medical Supplies': (camp.medical_supplies, camp.max_medical_supplies),
                'Shelter': (camp.max_shelter, camp.max_shelter)
            }

            resource_labels = {}

            for resource_name, (amount, capacity) in resources.items():
                resource_frame = tk.Frame(parent)
                resource_frame.pack(fill='x', expand=True)

                tk.Label(resource_frame, text=f"{resource_name}:").pack(side='left')
                amount_label = tk.Label(resource_frame, text=f"{amount}/{capacity}")
                amount_label.pack(side='left')
                resource_labels[resource_name] = amount_label

                def update_resource(resource_name, increment):
                    current_amount, current_capacity = resources[resource_name]
                    new_amount = max(0, min(current_amount + increment, current_capacity))  

                    if resource_name == 'Water':
                        camp.water = new_amount
                    elif resource_name == 'Food':
                        camp.food = new_amount
                    elif resource_name == 'Medical Supplies':
                        camp.medical_supplies = new_amount
                    elif resource_name == 'Shelter':
                        camp.shelter = new_amount

                    self.update_camp(camp.campID, water=camp.water, food=camp.food, 
                                    medical_supplies=camp.medical_supplies, shelter=camp.shelter)

                    amount_label = resource_labels[resource_name]
                    amount_label.config(text=f"{new_amount}/{current_capacity}")

                increase_button = tk.Button(resource_frame, text="+", command=lambda res=resource_name: update_resource(res, 1))
                decrease_button = tk.Button(resource_frame, text="-", command=lambda res=resource_name: update_resource(res, -1))

                increase_button.pack(side='left')
                decrease_button.pack(side='left')


class VolunteerDashboard(Dashboard):
    """
    Takes in a volunteer object and displays a dashboard with information on that volunteer's camp.

    """
    def setup_dashboard(self, volunteer):
        #logic.getcamp are functions that fetch volunteer and camp data
        self.volunteer = volunteer
        # Directly using camp1 for this example
        self.camp = CampDataRetrieve.get_camp('campID',volunteer.campID)[0]

        # Create and add a new tab for the volunteer's camp
        self.tab_control = ttk.Notebook(self)
        camp_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(camp_tab, text=f'Camp {self.camp.campID}')
        self.tab_control.pack(expand=1, fill="both")

        # Populate the newly created tab with camp information
        self.populate_camp_tab(camp_tab, self.camp)

class AdminDashboard(Dashboard):
    """
    Takes in a list of camp objects TBD and displays a dashboard with information on each camp.
    
    Includes an overview tab with information on all camps + additional resources. Also incudes a tab for each invidual camp.
    """
    
    def setup_dashboard(self, plan):
        self.planCamps = CampDataRetrieve.get_camp('planID',plan.planID)[0]
        self.additional_resources = {'Food': [40, 100], 'Water': [30, 80], 'Medicine': [10, 60], 'Shelter': [10,90]} 
        self.create_admin_tabs(self.planCamps, self.additional_resources)
    
    def create_admin_tabs(self, planCamps, additional_resources):
        self.planCamps = planCamps
        self.tab_control = ttk.Notebook(self)
        self.overview_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text='Overview')
        self.populate_overview_tab(self.overview_tab, self.planCamps, additional_resources)
        for camp in self.planCamps:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=f'Camp {camp.campID}')
            self.populate_camp_tab(tab, camp)
        self.tab_control.pack(expand=1, fill="both")

    def populate_overview_tab(self, tab, planCamps, additional_resources):
        camps_frame = tk.Frame(tab)
        camps_frame.pack(side='left', fill='both', expand=True)

        for camp in planCamps:
            camp_frame = tk.Frame(camps_frame, borderwidth=1, relief='solid')
            camp_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            tk.Label(camp_frame, text=f"Camp {camp.campID}", font=('Arial', 16, 'bold')).pack(pady=(5, 10))

            self.create_resource_frame(camp_frame, camp)

            ttk.Button(camp_frame, text="Edit Camp", command=lambda cn=camp: self.show_screen('EditCamp', cn)).pack(pady=5)

        additional_resources_frame = tk.Frame(tab, bg='lightgray', bd=2, relief='groove')
        additional_resources_frame.pack(side='right', fill='y', padx=(5, 0))
        tk.Label(additional_resources_frame, text="Additional Resources Available", bg='lightgray').pack(pady=10)

        self.create_resource_frame(additional_resources_frame, additional_resources)
