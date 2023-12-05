import tkinter as tk
from tkinter import ttk
from dummydata import camp1, camp2, camp3
from dummydata import refugee1, refugee2


class Dashboard(tk.Frame):
    def __init__(self, root, show_screen, screen_data, *args):
        super().__init__(root)
        self.root = root
        self.setup_dashboard(screen_data)
        self.show_screen = show_screen

    def setup_dashboard(self, *args):
        raise NotImplementedError("Subclasses should implement this method to setup the dashboard layout")
    
    
    def populate_camp_tab(self, tab, camp):
        print(f"Populating tab for Camp ID: {camp.campID}")

        # Split the frame into left and right sections
        left_frame = tk.Frame(tab, bg='white')
        right_frame = tk.Frame(tab, bg='white')
        left_frame.pack(side='left', fill='both', expand=True)
        right_frame.pack(side='right', fill='both', expand=True)

        self.create_resource_frame(left_frame, camp)

        ttk.Button(left_frame, text="Edit Camp", command=lambda: self.show_screen('EditCamp', camp.campID)).pack(pady=5)

        # Create refugees section in right frame
        self.create_refugees_section(right_frame, camp)

    def create_refugees_section(self, parent, camp):
        refugees_title = tk.Label(parent, text=f"Refugees in Camp {camp.campID}", font=('Arial', 16, 'bold'))
        refugees_title.pack(pady=10)

        # Search and filter frame
        search_frame = tk.Frame(parent, bg='white')
        search_frame.pack(pady=5, fill='x')
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side='left', padx=5, expand=True, fill='x')

        filter_button = ttk.Button(search_frame, text="Filter/Search", command=self.update_refugees_list(search_entry))
        filter_button.pack(side='left', padx=5)

        self.refugees_listbox = tk.Listbox(parent)
        self.refugees_listbox.pack(pady=10, expand=True, fill='both')

        try:
            # Fetch and display refugees based on filter and value
            self.update_refugees_list(search_entry)()
        except Exception as e:
            pass

        manage_refugees_button = ttk.Button(parent, text="Manage Refugees", command=lambda: self.show_screen('RefugeeList', self.camp))
        manage_refugees_button.pack(pady=5)

    def update_refugees_list(self,search_entry):
        def update():
            filter_type = 'camp' if not search_entry.get() else 'name'
            filter_value = self.camp.campID if not search_entry.get() else search_entry.get()

            try:
                self.refugees = [refugee1, refugee2]  # placeholder
                # self.refugees = self.data_access.get_refugees(filter_type, filter_value)
                self.refugees_listbox.delete(0, tk.END)

                for refugee in self.refugees:
                    listbox_entry = f"{refugee.first_name} {refugee.last_name} - {refugee.medical_condition}"
                    self.refugees_listbox.insert(tk.END, listbox_entry)

                    # Bind the double-click event to a lambda function
                    self.refugees_listbox.bind('<Double-1>', lambda event, r=refugee: self.on_refugee_double_click(r))
            except Exception as e:
                self.show_error_message(f"Error fetching refugees: {str(e)}")

        return update


    def on_refugee_double_click(self, refugee):
        index = self.refugees_listbox.curselection()
        if index:
            selected_index = index[0]
            selected_refugee = self.refugees[selected_index]
            self.show_screen('EditRefugee', selected_refugee)


    def create_resource_frame(self, parent, camp):
        resources = {
            'Water': (camp.water, camp.max_water),
            'Food': (camp.food, camp.max_food),
            'Medical Supplies': (camp.medical_supplies, camp.max_medical_supplies),
            'Shelter': (camp.shelter, camp.max_shelter)
        }

        for resource_name, (amount, capacity) in resources.items():
            resource_frame = tk.Frame(parent)
            resource_frame.pack(fill='x', expand=True)

            tk.Label(resource_frame, text=f"{resource_name}:").pack(side='left')
            amount_label = tk.Label(resource_frame, text=f"{amount}/{capacity}")
            amount_label.pack(side='left')

            # ttk.Button(resource_frame, text="-", width=2, command=...).pack(side='left')
            # ttk.Button(resource_frame, text="+", width=2, command=...).pack(side='left')


class VolunteerDashboard(Dashboard):
    def setup_dashboard(self, volunteer):
        #logic.getcamp are functions that fetch volunteer and camp data
        # self.Camp = logic.getcamp(volunteer)

        # Directly using camp1 for this example
        self.camp = camp1

        # Create and add a new tab for the volunteer's camp
        self.tab_control = ttk.Notebook(self)
        camp_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(camp_tab, text=f'Camp {self.camp.campID}')
        self.tab_control.pack(expand=1, fill="both")

        # Populate the newly created tab with camp information
        self.populate_camp_tab(camp_tab, self.camp)

class AdminDashboard(Dashboard):
    def setup_dashboard(self, planCamps):
        self.planCamps = [camp1, camp2, camp3]  # placeholders
        self.additional_resources = {'Food': [40, 100], 'Water': [30, 80], 'Medicine': [10, 60], 'Shelter': [10,90]} #placeholders
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

            ttk.Button(camp_frame, text="Edit Camp", command=lambda cn=camp.campID: self.show_screen('EditCamp', cn)).pack(pady=5)

        additional_resources_frame = tk.Frame(tab, bg='lightgray', bd=2, relief='groove')
        additional_resources_frame.pack(side='right', fill='y', padx=(5, 0))
        tk.Label(additional_resources_frame, text="Additional Resources Available", bg='lightgray').pack(pady=10)

        self.create_resource_frame(additional_resources_frame, camp1)
