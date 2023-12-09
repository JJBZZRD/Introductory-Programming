import tkinter as tk
from tkinter import ttk

from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
from ..Logic.camp_data_edit import CampDataEdit
from ..Logic.plan_data_retrieve import PlanDataRetrieve
from ..Logic.plan_data_edit import PlanEdit

class Dashboard(tk.Frame):
    def __init__(self, ui_manager, *args):
        super().__init__(ui_manager.root)
        self.root = ui_manager.root
        self.setup_dashboard(ui_manager.screen_data)
        self.show_screen = ui_manager.show_screen

    def setup_dashboard(self, *args):
        raise NotImplementedError("Subclasses should implement this method to setup the dashboard layout")

    def setup_camp_tab(self, parent_tab, camp, plan, type):
        self.create_title_frame(parent_tab, camp)

        resources_frame = self.create_resources_section(parent_tab, camp, plan, type)
        statistics_frame = self.create_camp_statistics_section(parent_tab, camp)
        refugees_volunteers_frame = self.create_camp_refugees_volunteers_section(parent_tab, camp, 'refugees', type)

        resources_frame.grid(row=1, column=0, sticky="nsew")
        statistics_frame.grid(row=1, column=1, sticky="nsew")
        refugees_volunteers_frame.grid(row=1, column=2, sticky="nsew")
        parent_tab.grid_columnconfigure(0, weight=1)
        parent_tab.grid_columnconfigure(1, weight=1)
        parent_tab.grid_columnconfigure(2, weight=1)
        parent_tab.grid_rowconfigure(1, weight=1)
        
    def create_title_frame(self, parent_tab, camp):
        title_frame = tk.Frame(parent_tab, bg='white', height=30)
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=2)
        title_frame.grid_propagate(False)

        current_capacity = CampDataRetrieve.get_camp(campID=camp.campID)[0].max_shelter
        
        title_text = f"Details for Camp {camp.campID} - Capacity: placeholder/{current_capacity}"
        title_label = tk.Label(title_frame, text=title_text, font=('Arial', 16, 'bold'), bg='white')
        title_label.pack(side='left', padx=10)
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        
    def create_camp_statistics_section(self, parent_tab, camp):
        statistics_frame = tk.Frame(parent_tab, bg='white')
        
        statistics_frame.grid(row=1, column=1, sticky="nsew", pady=5)
        
        statistics_title = tk.Label(statistics_frame, text="Statistics:")
        statistics_title.grid(row=0, column=0, sticky="w") 
        
        self.populate_statistics_section(statistics_frame, camp)

        return statistics_frame

    def populate_statistics_section(self, statistics_frame, camp):
        def get_number_of_families():
            return 0

        def get_average_age():
            return 0

        def get_number_of_dead():
            return 0

        tk.Label(statistics_frame, text="Number of families:").grid(row=1, column=0, sticky="w")
        tk.Label(statistics_frame, text=str(get_number_of_families())).grid(row=1, column=1)

        tk.Label(statistics_frame, text="Average age:").grid(row=2, column=0, sticky="w")
        tk.Label(statistics_frame, text=str(get_average_age())).grid(row=2, column=1)

        tk.Label(statistics_frame, text="Dead:").grid(row=3, column=0, sticky="w")
        tk.Label(statistics_frame, text=str(get_number_of_dead())).grid(row=3, column=1)

    def create_resources_section(self, parent_tab, camp, plan, user_type):
        resources_frame = tk.Frame(parent_tab, bg='white')

        camp_resources_estimation = CampDataRetrieve.get_camp_resources(camp.campID)
        
        # Initial resources are only those belonging to the camp
        resources = {
            'Water': camp.water,
            'Food': camp.food,
            'Medical Supplies': camp.medical_supplies,
            'Max shelter': camp.max_shelter,
        }

        # Add additional resources for admin
        if user_type == 'admin' and plan:
            resources.update({
                'Additional Water': plan.water,
                'Additional Food': plan.food,
                'Additional Medical Supplies': plan.medical_supplies,
                'Additional Shelter': plan.shelter,
            })

        for index, (resource_name, amount) in enumerate(resources.items()):
            resource_frame = tk.Frame(resources_frame)
            resource_frame.grid(row=index, column=0, sticky="ew")

            top_frame = tk.Frame(resource_frame)
            top_frame.grid(row=0, column=0, sticky="ew")

            tk.Label(top_frame, text=f"{resource_name}:").grid(row=0, column=0, sticky="w")
            amount_label = tk.Label(top_frame, text=str(amount))
            amount_label.grid(row=0, column=1)

            # Add buttons for volunteers and admin
            if user_type in ['volunteer', 'admin'] and resource_name in ['Water', 'Food', 'Medical Supplies', 'Max shelter']:
                tk.Button(top_frame, text="-", command=lambda resource_name=resource_name, resource_frame=resource_frame: self.update_resource(camp, resource_frame, resource_name, -1, plan, user_type)).grid(row=0, column=2)
                tk.Button(top_frame, text="+", command=lambda resource_name=resource_name, resource_frame=resource_frame: self.update_resource(camp, resource_frame, resource_name, 1, plan, user_type)).grid(row=0, column=3)

            bottom_frame = tk.Frame(resource_frame)
            bottom_frame.grid(row=1, column=0, sticky="ew")

            # Display 'Days left' only for specific resources
            if resource_name in ['Water', 'Food', 'Medical Supplies']:
                days_left = camp_resources_estimation.get(resource_name)                
                tk.Label(bottom_frame, text=f"Days left: {days_left}").grid(row=0, column=0, sticky="w")

        return resources_frame


    def update_resource(self, camp, resource_frame, resource_name, increment, plan, type):
        print(f"Updating {resource_name} by {increment} in resource frame {resource_frame} for camp {camp.campID}, plan {plan.planID}")
        
        resource_key = resource_name.lower().replace(' ', '_')
        if type == 'admin' and resource_name.startswith('Additional'):
            current_amount = getattr(plan, resource_key)
            new_amount = max(0, current_amount + increment)
    
            if PlanEdit.update_plan(plan.planID, **{resource_key: new_amount}):
                setattr(plan, resource_key, new_amount)
        else:
            current_amount = getattr(camp, resource_key)
            new_amount = max(0, current_amount + increment)
            if CampDataEdit.update_camp(camp.campID, **{resource_key: new_amount}):
                print (f"Updating {resource_key} to {new_amount}")
                setattr(camp, resource_key, new_amount)

        top_frame = resource_frame.winfo_children()[0]
        amount_label = top_frame.winfo_children()[1]
        amount_label.config(text=str(new_amount))

        camp_resources_estimation = CampDataRetrieve.get_camp_resources(camp.campID)
        resource_order = ['Water', 'Food', 'Medical Supplies']
        if resource_name in resource_order:
            days_left = camp_resources_estimation.get(resource_name)

            bottom_frame = resource_frame.winfo_children()[1]
            days_left_label = bottom_frame.winfo_children()[0]
            days_left_label.config(text=f"Days left: {days_left}")

        resource_frame.update()

    
    def create_camp_refugees_volunteers_section(self, parent_tab, camp, display_type, user_type):
        refugees_volunteers_frame = tk.Frame(parent_tab, bg='white')
        refugees_volunteers_frame.grid(row=1, column=2, sticky="nsew", pady=5)  

        title_text = f"{'Refugees' if display_type == 'refugees' else 'Volunteers'} in Camp {camp.campID}"
        columns = ("Name", "Triage Category") if display_type == "refugees" else ("Name", "Camp")
        update_list_func = self.update_refugees_list if display_type == 'refugees' else self.update_volunteers_list
        manage_screen = "RefugeeList" if display_type == 'refugees' else "VolunteerList"
        double_click_func = self.on_refugee_double_click if display_type == 'refugees' else self.on_volunteer_double_click

        refugees_title = tk.Label(refugees_volunteers_frame, text=title_text, font=('Arial', 16, 'bold'))
        refugees_title.grid(row=0, column=0, sticky="w", pady=10)

        search_frame = tk.Frame(refugees_volunteers_frame, bg='white')
        search_frame.grid(row=1, column=0, sticky="ew", pady=5)
        search_entry = tk.Entry(search_frame)
        search_entry.grid(row=0, column=0, sticky="ew", padx=5)
        search_frame.grid_columnconfigure(0, weight=1)

        refugees_treeview = ttk.Treeview(refugees_volunteers_frame, columns=columns)
        refugees_treeview.grid(row=2, column=0, sticky="nsew", pady=10)
        refugees_volunteers_frame.grid_rowconfigure(2, weight=1)

        refugees_treeview.bind("<Double-1>", lambda event: double_click_func(event, refugees_treeview))

        for col in columns:
            refugees_treeview.heading(col, text=col)
            refugees_treeview.column(col, width=150)

        filter_button = ttk.Button(search_frame, text="Filter/Search", command=lambda: update_list_func(camp, search_entry, refugees_treeview))
        filter_button.grid(row=0, column=1, padx=3)

        update_list_func(camp, search_entry, refugees_treeview)

        if user_type == 'admin' or (user_type == 'volunteer' and display_type == 'volunteers'):
            manage_button = ttk.Button(refugees_volunteers_frame, text=f"Manage {display_type.capitalize()}", command=lambda: self.show_screen(manage_screen, camp))
            manage_button.grid(row=3, column=0, pady=5)

        return refugees_volunteers_frame

    def update_refugees_list(self, camp, search_entry, refugees_treeview):
        filter_value = search_entry.get().strip()

        refugees_treeview.delete(*refugees_treeview.get_children())
            
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
            
    def update_volunteers_list(self, camp, search_entry, volunteers_treeview):
        filter_value = search_entry.get().strip()

        volunteers_treeview.delete(*volunteers_treeview.get_children())

        self.volunteers = PersonDataRetrieve.get_volunteers(camp_id=camp.campID, name=filter_value)

        if not self.volunteers:
            volunteers_treeview.insert("", "end", text="No matching volunteers found.")
        else:
            for volunteer in self.volunteers:
                volunteers_treeview.insert("", "end", text=volunteer.volunteerID, values=(f"{volunteer.first_name} {volunteer.last_name}", volunteer.role))

    def on_volunteer_double_click(self, _, treeview):
        item = treeview.focus()
        if item:
            selected_volunteer = self.volunteers[int(treeview.item(item, "text")) - 1]
        self.show_screen('EditVolunteer', selected_volunteer)

class VolunteerDashboard(Dashboard):
    """
    Takes in a volunteer object and displays a dashboard with information on that volunteer's camp.

    """
    def setup_dashboard(self, volunteer):
        self.camp = CampDataRetrieve.get_camp(campID=volunteer.campID)[0]
        self.plan = PlanDataRetrieve.get_plan(planID=self.camp.planID)[0]

        self.tab_control = ttk.Notebook(self)
        camp_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(camp_tab, text=f'Camp {self.camp.campID}')
        self.tab_control.pack(expand=1, fill="both")

        self.setup_camp_tab(camp_tab, self.camp, self.plan, 'volunteer')

class AdminDashboard(Dashboard):
    """
    Admin dashboard for displaying information on each camp and additional resources.
    Includes an overview tab with information on all camps plus additional resources, 
    as well as individual tabs for each camp, a resource distribution tab, and a statistics tab.
    """

    def setup_dashboard(self, plan):
        # Assuming admin has access to all camps or specific camps
        self.plan = plan
        self.planCamps = CampDataRetrieve.get_all_camps()  # or a filtered list based on admin access

        self.tab_control = ttk.Notebook(self)

        # Set up individual tabs
        self.create_admin_tabs()

        self.tab_control.pack(expand=1, fill="both")

    def create_admin_tabs(self):
        # Setup for camp tabs
        self.setup_camp_tabs()

        # Setup for additional tabs
        self.setup_distribute_resources_tab()
        self.setup_plan_statistics_tab()

    def setup_camp_tabs(self):
        user_type = 'admin'
        for camp in self.planCamps:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=f'Camp {camp.campID}')
            self.setup_camp_tab(tab, camp, self.plan, user_type)

    def setup_distribute_resources_tab(self):
        distribute_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(distribute_tab, text='Distribute Plan Resources')

        canvas = tk.Canvas(distribute_tab)
        scrollbar = ttk.Scrollbar(distribute_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for camp in self.planCamps:
            camp_resources_frame = self.create_resources_section(scrollable_frame, camp, self.plan, 'admin')
            camp_resources_frame.pack(fill='x', expand=True, padx=10, pady=5)

        # Pack everything into the tab
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_plan_statistics_tab(self):
        stats_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(stats_tab, text='Plan Camps Statistics')

    
    # def populate_overview_tab(self, tab):
    #     self.create_camps_frame(tab, self.planCamps)
    #     self.create_additional_resources_frame(tab, self.plan, self.additional_resources)
    
    # def create_camps_frame(self, parent, planCamps):
    #     camps_frame = tk.Frame(parent, bg='white')
    #     camps_frame.pack(side='left', fill='both', expand=True)

    #     for camp in planCamps:
    #         camp_frame = tk.Frame(camps_frame, bg='white', borderwidth=1, relief='solid', padx=5, pady=5)
    #         camp_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
    #         tk.Label(camp_frame, text=f"Camp {camp.campID}", font=('Arial', 16, 'bold')).pack(pady=(5, 10))
    #         self.populate_resource_frame(camp_frame, camp)
    #         ttk.Button(camp_frame, text="Edit Camp", style='TButton').pack(pady=5)

    # def create_additional_resources_frame(self, parent, plan, additional_resources):
    #     resources_frame = tk.Frame(parent, bg='white', bd=2, relief='groove')
    #     resources_frame.pack(side='right', fill='y', padx=(5, 0))
    #     tk.Label(resources_frame, text="Additional Resources Available", bg='white', font=('Arial', 14)).pack(pady=10)
    #     for resource_name, amount in additional_resources.items():
    #         self.create_resource_amount_frame(resources_frame, plan, resource_name, amount, self.update_additional_resource)

    # def create_resource_amount_frame(self, frame, plan, resource_name, amount, update_additional_resource):
    #     top_frame = tk.Frame(frame, bg='white')
    #     top_frame.pack(fill='x', expand=True)
    #     tk.Label(top_frame, text=f"{resource_name}:", bg='white', font=('Arial', 12)).pack(side='left')
    #     label = tk.Label(top_frame, text=str(amount), bg='white')
    #     label.pack(side='left')
    #     tk.Button(top_frame, text="+", command=lambda: update_additional_resource(label, plan, resource_name, 1)).pack(side='left')
    #     tk.Button(top_frame, text="-", command=lambda: update_additional_resource(label, plan, resource_name, -1)).pack(side='left')

    # def update_additional_resource(self, label, plan, resource_name, increment):
    #         self.plan = plan
    #         current_amount = self.additional_resources[resource_name]
    #         new_amount = max(0, current_amount + increment)
    #         self.additional_resources[resource_name] = new_amount
    #         label.config(text=str(new_amount))

    #         try:
    #             PlanEdit.update_plan(
    #                 planID=self.plan.planID,
    #                 water=self.additional_resources.get('Water'),
    #                 food=self.additional_resources.get('Food'),
    #                 shelter=self.additional_resources.get('Shelter'),
    #                 medical_supplies=self.additional_resources.get('Medical Supplies')
    #             )
    #         except Exception as e:
    #             print(f"Error updating plan: {e}")
    #             # Consider adding user feedback here, e.g., displaying an error message in the UI.