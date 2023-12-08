import tkinter as tk
from tkinter import ttk

from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.camp_data_edit import CampDataEdit
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

        refugees_frame = tk.Frame(left_frame, bg='white')
        refugees_frame.pack(fill='x', pady=5)
        
        current_capacity = CampDataRetrieve.get_camp(campID=camp.campID)[0].max_shelter
        refugees_title = tk.Label(refugees_frame, text="Capacity usage: placeholder/" + str(current_capacity))
        refugees_title.pack(side='top')

        middle_section = tk.Frame(left_frame, bg='white')
        middle_section.pack(fill='x', pady=5)

        resources_frame = tk.Frame(middle_section, bg='white')
        resources_frame.pack(side='left', fill='y', expand=True)
        resources_title = tk.Label(resources_frame, text="Resources:")
        resources_title.pack(side='top')
        self.populate_resource_frame(resources_frame, camp)

        statistics_frame = tk.Frame(middle_section, bg='white')
        statistics_frame.pack(side='right', fill='y', expand=True)
        statistics_title = tk.Label(statistics_frame, text="Statistics:")
        statistics_title.pack(side='top')
        self.populate_statistics_frame(statistics_frame, camp)

        ttk.Button(left_frame, text="Edit Camp", command=lambda: self.show_screen('EditCamp', camp)).pack(pady=5)
        self.populate_refugees_section(right_frame, camp)
        ttk.Button(right_frame, text="Manage Refugees", command=lambda: self.show_screen('RefugeesList', camp)).pack(pady=5)


    def populate_refugees_section(self, parent, camp):
        refugees_title = tk.Label(parent, text=f"Refugees in Camp {camp.campID}", font=('Arial', 16, 'bold'))
        refugees_title.pack(pady=10)
        
        search_frame = tk.Frame(parent, bg='white')
        search_frame.pack(pady=5, fill='x')

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        refugees_treeview = ttk.Treeview(parent, columns=("Name", "Medical Condition"))
        
        filter_button = ttk.Button(search_frame, text="Filter/Search", command=lambda: self.update_refugees_list(camp, search_entry, refugees_treeview))
        filter_button.pack(side='left', padx=5)

        refugees_treeview.pack(pady=10, expand=True, fill='both')
        refugees_treeview.bind('<Double-1>', lambda event, tv=refugees_treeview: self.on_refugee_double_click(event, tv))

        refugees_treeview.heading("#0", text="ID")
        refugees_treeview.column("#0", width=50, anchor='center')
        refugees_treeview.heading("Name", text="Name")
        refugees_treeview.column("Name", width=150)
        refugees_treeview.heading("Medical Condition", text="Medical Condition")
        refugees_treeview.column("Medical Condition", width=150)

        self.update_refugees_list(camp, search_entry, refugees_treeview)
        
        refugees_treeview.column("#0", width=150, anchor='center')
        refugees_treeview.heading("Name", text="Name")
        refugees_treeview.column("Name", width=150)
        refugees_treeview.heading("Medical Condition", text="Medical Condition")
        refugees_treeview.column("Medical Condition", width=150)

        self.update_refugees_list(camp, search_entry, refugees_treeview) 

    def update_refugees_list(self, camp, search_entry, refugees_treeview):
        filter_value = search_entry.get().strip()

        print(camp.campID)
            
        self.refugees = PersonDataRetrieve.get_refugees(camp_id=camp.campID, name=filter_value)

        if not self.refugees:
            refugees_treeview.insert("", "end", text="No matching refugees found.")
        else:
            for refugee in self.refugees:
                print(refugee.__dict__) 
                refugees_treeview.insert("", "end", text=refugee.refugeeID, values=(f"{refugee.first_name} {refugee.last_name}", refugee.triage_category))
    
    def on_refugee_double_click(self, _, treeview):
        item = treeview.focus()
        if item:
            selected_refugee = self.refugees[int(treeview.item(item, "text")) - 1]
            self.show_screen('EditRefugee', selected_refugee)
        

    def populate_resource_frame(self, parent, camp):
        camp_resources_estimation = CampDataRetrieve.get_camp_resources(camp.campID)
        resources = {
            'Water': camp.water,
            'Food': camp.food,
            'Medical Supplies': camp.medical_supplies,
        }

        def create_resource_frame(resource_name, amount, index):
            resource_frame = tk.Frame(parent)
            resource_frame.pack(fill='x', expand=True)

            create_resource_amount_frame(resource_frame, resource_name, amount)
            create_days_left_frame(resource_frame, resource_name, index)

        def create_resource_amount_frame(frame, resource_name, amount):
            top_frame = tk.Frame(frame)
            top_frame.pack(fill='x', expand=True)

            tk.Label(top_frame, text=f"{resource_name}:").pack(side='left')
            tk.Label(top_frame, text=str(amount)).pack(side='left')
                        
            tk.Button(top_frame, text="-", command=lambda: self.update_resource(camp, frame, resource_name, -1)).pack(side='left')
            tk.Button(top_frame, text="+", command=lambda: self.update_resource(camp, frame, resource_name, 1)).pack(side='left')

        def create_days_left_frame(frame, resource_name, index):
            bottom_frame = tk.Frame(frame)
            bottom_frame.pack(fill='x', expand=True)

            days_left = camp_resources_estimation[index] if index < len(camp_resources_estimation) else "N/A"
            tk.Label(bottom_frame, text=f"Days of {resource_name} Left: {days_left}").pack(side='left')

        for index, (resource_name, amount) in enumerate(resources.items()):
            create_resource_frame(resource_name, amount, index)

    def update_resource(self, camp, resource_frame, resource_name, increment):
        resource_key = resource_name.lower().replace(' ', '_')
        current_amount = getattr(camp, resource_key)
        new_amount = max(0, current_amount + increment)

        if CampDataEdit.update_camp(camp.campID, **{resource_key: new_amount}):
            setattr(camp, resource_key, new_amount)


            top_frame = resource_frame.winfo_children()[0]
            amount_label = top_frame.winfo_children()[1]
            amount_label.config(text=str(new_amount))

            camp_resources_estimation = CampDataRetrieve.get_camp_resources(camp.campID)
            resource_order = ['Water', 'Food', 'Medical Supplies']
            if resource_name in resource_order:
                index = resource_order.index(resource_name)
                days_left = camp_resources_estimation[index] if index < len(camp_resources_estimation) else "N/A"

                bottom_frame = resource_frame.winfo_children()[1]
                days_left_label = bottom_frame.winfo_children()[0]
                days_left_label.config(text=f"Days of {resource_name} Left: {days_left}")

            resource_frame.update()

            
    def populate_statistics_frame(self, parent, camp):
        statistics_frame = tk.Frame(parent)
        statistics_frame.pack(fill='x', expand=True)

        # Dummy functions to be filled in later
        def get_number_of_families():
            return 0

        def get_average_age():
            return 0

        def get_number_of_dead():
            return 0

        tk.Label(statistics_frame, text="Number of families:").grid(row=0, column=0)
        tk.Label(statistics_frame, text=get_number_of_families()).grid(row=0, column=1)

        tk.Label(statistics_frame, text="Average age:").grid(row=1, column=0)
        tk.Label(statistics_frame, text=get_average_age()).grid(row=1, column=1)

        tk.Label(statistics_frame, text="Dead:").grid(row=2, column=0)
        tk.Label(statistics_frame, text=get_number_of_dead()).grid(row=2, column=1)

        # Populate the labels with the dummy functions
class VolunteerDashboard(Dashboard):
    """
    Takes in a volunteer object and displays a dashboard with information on that volunteer's camp.

    """
    def setup_dashboard(self, volunteer):
        print(" ========= setup_dashboard ============ ")
        self.volunteer = volunteer
        print(volunteer.display_info())
        print(volunteer.campID)
        camp = CampDataRetrieve.get_camp(campID=volunteer.campID)[0]
        print(camp.display_info)
        self.camp = CampDataRetrieve.get_camp(campID=volunteer.campID)[0]

        self.tab_control = ttk.Notebook(self)
        camp_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(camp_tab, text=f'Camp {self.camp.campID}')
        self.tab_control.pack(expand=1, fill="both")

        self.populate_camp_tab(camp_tab, self.camp)

class AdminDashboard(Dashboard):
    """
    Takes in a list of camp objects TBD and displays a dashboard with information on each camp.
    
    Includes an overview tab with information on all camps + additional resources. Also incudes a tab for each invidual camp.
    """
    
    def setup_dashboard(self, plan):
        self.plan = plan
        self.planCamps = CampDataRetrieve.get_camp(planID=plan.planID)
        
        additional_resources_list = PlanDataRetrieve.get_resources(plan.planID)

        self.additional_resources = {
            'Food': additional_resources_list[0],
            'Water': additional_resources_list[1],
            'Shelter': additional_resources_list[2],
            'Medical Supplies': additional_resources_list[3],
        }

        self.create_admin_tabs(self.planCamps, plan, self.additional_resources)        
    
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
        self.create_camps_frame(tab, planCamps)
        self.create_additional_resources_frame(tab, additional_resources)

    def create_camps_frame(self, parent, planCamps):
        camps_frame = tk.Frame(parent, bg='lightgray')
        camps_frame.pack(side='left', fill='both', expand=True)

        for camp in planCamps:
            camp_frame = tk.Frame(camps_frame, bg='white', borderwidth=1, relief='solid', padx=5, pady=5)
            camp_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
            tk.Label(camp_frame, text=f"Camp {camp.campID}", font=('Arial', 16, 'bold')).pack(pady=(5, 10))
            self.populate_resource_frame(camp_frame, camp)
            ttk.Button(camp_frame, text="Edit Camp", style='TButton').pack(pady=5)

    def create_additional_resources_frame(self, parent, additional_resources):
        resources_frame = tk.Frame(parent, bg='lightgray', bd=2, relief='groove')
        resources_frame.pack(side='right', fill='y', padx=(5, 0))
        tk.Label(resources_frame, text="Additional Resources Available", bg='lightgray', font=('Arial', 14)).pack(pady=10)
        for resource_name, amount in additional_resources.items():
            self.create_resource_amount_frame(resources_frame, resource_name, amount, self.update_additional_resource)

    def create_resource_amount_frame(self, frame, resource_name, amount, update_additional_resource):
        top_frame = tk.Frame(frame, bg='lightgray')
        top_frame.pack(fill='x', expand=True)
        tk.Label(top_frame, text=f"{resource_name}:", bg='lightgray', font=('Arial', 12)).pack(side='left')
        label = tk.Label(top_frame, text=str(amount), bg='lightgray')
        label.pack(side='left')
        tk.Button(top_frame, text="+", command=lambda: update_additional_resource(label, resource_name, 1)).pack(side='left')
        tk.Button(top_frame, text="-", command=lambda: update_additional_resource(label, resource_name, -1)).pack(side='left')

    def update_additional_resource(self, label, resource_name, increment):
        current_amount = self.additional_resources[resource_name]
        new_amount = max(0, current_amount + increment)
        self.additional_resources[resource_name] = new_amount

        label.config(text=str(new_amount))

        # Add code here to persist the updated additional resources to the database 

