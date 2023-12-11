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
        raise NotImplementedError(
            "Subclasses should implement this method to setup the dashboard layout"
        )

    def setup_camp_tab(self, parent_tab, camp, plan, type):
        self.create_camp_title_frame(parent_tab, plan, camp)

        resources_frame = self.create_resources_section(parent_tab, camp, plan, type)
        statistics_frame = self.create_camp_statistics_section(parent_tab, camp)
        refugees_volunteers_frame = self.create_camp_refugees_volunteers_section(
            parent_tab, camp, "refugees", type
        )

        resources_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        statistics_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        refugees_volunteers_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        parent_tab.grid_columnconfigure(0, weight=1)
        parent_tab.grid_columnconfigure(1, weight=1)
        parent_tab.grid_columnconfigure(2, weight=1)
        parent_tab.grid_rowconfigure(1, weight=1)

    def create_camp_title_frame(self, parent_tab, plan, camp):
        title_frame = tk.Frame(parent_tab, height=30)
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        title_frame.grid_propagate(False)
        title_frame.columnconfigure(0, weight=1)

        title_text = f"{plan.name} - Camp {camp.campID} - {camp.location}"
        title_label = tk.Label(title_frame, text=title_text, font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky="w", padx=10)

        edit_camp_button = ttk.Button(
            title_frame,
            text="Edit Camp",
            command=lambda: self.show_screen("EditCamp", camp),
        )
        edit_camp_button.grid(row=0, column=1, sticky="e", padx=10)

        title_frame.columnconfigure(1, weight=0)

    def create_camp_statistics_section(self, parent_tab, camp):
        camp_statistics_frame = tk.Frame(parent_tab)
        camp_statistics_frame.grid(row=0, column=0, sticky="ew")

        campID = camp.campID
        triage_stats = CampDataRetrieve.get_stats_triage_category(campID)
        gender_stats = CampDataRetrieve.get_stats_gender(campID)
        age_stats = CampDataRetrieve.get_stats_age(campID)
        vital_status_stats = CampDataRetrieve.get_stats_vital_status(campID)

        num_volunteers = len(PersonDataRetrieve.get_volunteers(campID=campID))
        num_refugees = len(PersonDataRetrieve.get_refugees(camp_id=campID))
        family_stats = CampDataRetrieve.get_stats_family(campID)
        num_families = (
            family_stats.get("num_families", "Error fetching families")
            if isinstance(family_stats, dict)
            else family_stats
        )

        stats_functions = [
            ("Gender Distribution", gender_stats),
            ("Age Distribution", age_stats),
            ("Vital Status", vital_status_stats),
            ("Triage Categories", triage_stats),
        ]

        row = 0

        tk.Label(
            camp_statistics_frame,
            text=f"Number of Volunteers: {num_volunteers}",
            font=("Arial", 11),
        ).grid(row=row, column=0, sticky="w")
        row += 1

        tk.Label(
            camp_statistics_frame,
            text=f"Number of Refugees: {num_refugees}",
            font=("Arial", 11),
        ).grid(row=row, column=0, sticky="w")
        row += 1

        tk.Label(
            camp_statistics_frame,
            text=f"Number of Families: {num_families}",
            font=("Arial", 11),
        ).grid(row=row, column=0, sticky="w")
        row += 1

        for label, stats in stats_functions:
            tk.Label(
                camp_statistics_frame, text=label, font=("Arial", 11, "bold")
            ).grid(row=row, column=0, sticky="w")
            row += 1

            if isinstance(stats, str):
                tk.Label(camp_statistics_frame, text=stats, font=("Arial", 11)).grid(
                    row=row, column=0, sticky="w"
                )
                row += 1
                continue

            for key, value in stats.items():
                if "num_" in key:
                    pct_key = "pct_" + key.split("_")[1]
                    pct_value = stats.get(pct_key, 0)
                    formatted_stat = (
                        f"{key.split('_')[1].title()}: {pct_value:.0f}% ({value})"
                    )
                    tk.Label(
                        camp_statistics_frame, text=formatted_stat, font=("Arial", 11)
                    ).grid(row=row, column=0, sticky="w")
                    row += 1

        return camp_statistics_frame

    def create_resources_section(
        self, parent_tab, camp, plan, user_type, additional_resources_frame=None
    ):
        resources_frame = tk.Frame(parent_tab)

        camp_resources_estimation = CampDataRetrieve.get_camp_resources(camp.campID)

        resources = {
            "Water": camp.water,
            "Food": camp.food,
            "Medical Supplies": camp.medical_supplies,
        }

        for index, (resource_name, amount) in enumerate(resources.items()):
            resource_frame = tk.Frame(resources_frame)
            resource_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=(5, 0))

            top_frame = tk.Frame(resource_frame)
            top_frame.grid(row=0, column=0, sticky="ew")
            top_frame.columnconfigure(0, weight=1)

            tk.Label(top_frame, text=f"{resource_name}:").grid(
                row=0, column=0, sticky="w"
            )
            amount_label = tk.Label(top_frame, text=str(amount))
            amount_label.grid(row=0, column=1)

            minus_button = tk.Button(
                top_frame,
                text="-",
                command=lambda resource_name=resource_name, resource_frame=resource_frame: self.update_resource(
                    camp,
                    resource_frame,
                    resource_name,
                    -10,
                    plan,
                    user_type,
                    additional_resources_frame=additional_resources_frame,
                ),
            )
            minus_button.grid(row=0, column=2, sticky="e")

            plus_button = tk.Button(
                top_frame,
                text="+",
                command=lambda resource_name=resource_name, resource_frame=resource_frame: self.update_resource(
                    camp,
                    resource_frame,
                    resource_name,
                    10,
                    plan,
                    user_type,
                    additional_resources_frame=additional_resources_frame,
                ),
            )
            plus_button.grid(row=0, column=3, sticky="e")

            bottom_frame = tk.Frame(resource_frame)
            bottom_frame.grid(row=1, column=0, sticky="ew")

            if resource_name in ["Water", "Food", "Medical Supplies", "Shelter"]:
                days_left = camp_resources_estimation.get(resource_name)
                tk.Label(bottom_frame, text=f"Days left: {days_left}\n").grid(
                    row=0, column=0, sticky="w"
                )

        return resources_frame

    def create_additional_resources_section(self, parent_frame, plan):
        additional_resources_frame = tk.Frame(parent_frame)

        additional_resources = {
            "Shelter": plan.shelter,
            "Water": plan.water,
            "Food": plan.food,
            "Medical Supplies": plan.medical_supplies,
        }

        for index, (resource_name, amount) in enumerate(additional_resources.items()):
            resource_frame = tk.Frame(additional_resources_frame)
            resource_frame.grid(row=index + 1, column=0, sticky="ew")

            top_frame = tk.Frame(resource_frame)
            top_frame.grid(row=0, column=0, sticky="ew")

            tk.Label(top_frame, text=f"{resource_name}:").grid(
                row=0, column=0, sticky="w"
            )

            amount_label = tk.Label(top_frame, text=str(amount))
            amount_label.grid(row=0, column=1)

            tk.Button(
                resource_frame,
                text="-",
                command=lambda res_name=resource_name, resource_frame=resource_frame: self.update_plan_resources(
                    resource_frame,
                    res_name,
                    plan,
                    -10,
                ),
            ).grid(row=0, column=2)

            tk.Button(
                resource_frame,
                text="+",
                command=lambda res_name=resource_name, resource_frame=resource_frame: self.update_plan_resources(
                    resource_frame,
                    res_name,
                    plan,
                    10,
                ),
            ).grid(row=0, column=3)

            bottom_frame = tk.Frame(resource_frame)
            bottom_frame.grid(row=1, column=0, sticky="ew")

        tk.Label(
            additional_resources_frame,
            text=f"\nButtons above update plan {self.plan.planID}'s \navailable additional resources.\n\nButtons under camp headings \ndistribute those additional \nresources",
            font=("Arial", 11, "bold"),
        ).grid(row=9, column=0, sticky="w")

        return additional_resources_frame

    def update_resource(
        self,
        camp,
        resource_frame,
        resource_name,
        increment,
        plan,
        user_type,
        additional_resources_frame=None,
    ):
        resource_key = resource_name.lower().replace(" ", "_")
        if user_type == "admin":
            plan_current_amount = getattr(plan, resource_key)
            new_plan_amount = max(0, plan_current_amount - increment)
            if PlanEdit.update_plan(plan.planID, **{resource_key: new_plan_amount}):
                setattr(plan, resource_key, new_plan_amount)

            if additional_resources_frame:
                for res_frame in additional_resources_frame.winfo_children():
                    top_frame = res_frame.winfo_children()[0]
                    res_name_label = top_frame.winfo_children()[0]
                    if res_name_label.cget("text") == f"{resource_name}:":
                        amount_label = top_frame.winfo_children()[1]
                        amount_label.config(text=str(new_plan_amount))
                        break

        camp_current_amount = getattr(camp, resource_key)
        new_camp_amount = max(0, camp_current_amount + increment)
        if CampDataEdit.update_camp(camp.campID, **{resource_key: new_camp_amount}):
            setattr(camp, resource_key, new_camp_amount)

        top_frame = resource_frame.winfo_children()[0]
        amount_label = top_frame.winfo_children()[1]
        amount_label.config(text=str(new_camp_amount))

        camp_resources_estimation = CampDataRetrieve.get_camp_resources(camp.campID)
        resource_order = ["Shelter", "Water", "Food", "Medical Supplies"]
        if resource_name in resource_order:
            days_left = camp_resources_estimation.get(resource_name)
            bottom_frame = resource_frame.winfo_children()[1]
            days_left_label = bottom_frame.winfo_children()[0]
            days_left_label.config(text=f"Days left: {days_left}\n")

        resource_frame.update()
        if additional_resources_frame:
            additional_resources_frame.update()

    def update_plan_resources(self, resource_frame, resource_name, plan, increment):
        resource_key = resource_name.lower().replace(" ", "_")
        current_amount = getattr(plan, resource_key)
        new_amount = max(0, current_amount + increment)
        if PlanEdit.update_plan(plan.planID, **{resource_key: new_amount}):
            setattr(plan, resource_key, new_amount)

        top_frame = resource_frame.winfo_children()[0]
        amount_label = top_frame.winfo_children()[1]
        amount_label.config(text=str(new_amount))

        resource_frame.update()

    def create_camp_refugees_volunteers_section(
        self, parent_tab, camp, display_type, user_type
    ):
        refugees_volunteers_frame = tk.Frame(parent_tab)
        refugees_volunteers_frame.grid(row=1, column=2, sticky="nsew", pady=5)

        title_text = f"{'Refugees' if display_type == 'refugees' else 'Volunteers'}"
        columns = (
            ("Name", "Medical status")
            if display_type == "refugees"
            else ("Name", "Phone number")
        )
        update_list_func = (
            self.update_refugees_list
            if display_type == "refugees"
            else self.update_volunteers_list
        )
        manage_screen = "RefugeeList" if display_type == "refugees" else "VolunteerList"
        double_click_func = (
            self.on_refugee_double_click
            if display_type == "refugees"
            else self.on_volunteer_double_click
        )

        refugees_title = tk.Label(
            refugees_volunteers_frame, text=title_text, font=("Arial", 14, "bold")
        )
        refugees_title.grid(row=0, column=0, sticky="w", pady=10)

        switch_button = tk.Button(
            refugees_volunteers_frame,
            text="Switch",
            command=lambda: self.create_camp_refugees_volunteers_section(
                parent_tab,
                camp,
                "volunteers" if display_type == "refugees" else "refugees",
                user_type,
            ),
        )
        switch_button.grid(
            row=0,
            column=0,
        )

        search_frame = tk.Frame(refugees_volunteers_frame)
        search_frame.grid(row=1, column=0, sticky="ew", pady=5)
        search_entry = tk.Entry(search_frame)
        search_entry.grid(row=0, column=0, sticky="ew", padx=5)
        search_frame.grid_columnconfigure(0, weight=1)

        refugees_treeview = ttk.Treeview(refugees_volunteers_frame, columns=columns)
        refugees_treeview.grid(row=2, column=0, sticky="nsew", pady=5)
        refugees_volunteers_frame.grid_rowconfigure(2, weight=1)

        refugees_treeview.bind(
            "<Double-1>", lambda event: double_click_func(event, refugees_treeview)
        )

        for col in columns:
            refugees_treeview.heading(col, text=col)
            refugees_treeview.column(col, width=150)

        filter_button = ttk.Button(
            search_frame,
            text="Filter/Search",
            command=lambda: update_list_func(camp, search_entry, refugees_treeview),
        )
        filter_button.grid(row=0, column=1, padx=3)

        update_list_func(camp, search_entry, refugees_treeview)

        manage_button = ttk.Button(
            refugees_volunteers_frame,
            text=f"Manage {display_type.capitalize()}",
            command=lambda: self.show_screen(manage_screen, camp),
        )
        manage_button.grid(row=3, column=0, pady=5)

        return refugees_volunteers_frame

    def update_refugees_list(self, camp, search_entry, refugees_treeview):
        filter_value = search_entry.get().strip()

        refugees_treeview.delete(*refugees_treeview.get_children())

        self.refugees = PersonDataRetrieve.get_refugees(
            camp_id=camp.campID, name=filter_value
        )

        if not self.refugees:
            refugees_treeview.insert("", "end", text="No matching refugees found.")
        else:
            for refugee in self.refugees:
                refugees_treeview.insert(
                    "",
                    "end",
                    text=refugee.refugeeID,
                    values=(
                        f"{refugee.first_name} {refugee.last_name}",
                        refugee.triage_category,
                    ),
                )

    def update_volunteers_list(self, camp, search_entry, volunteers_treeview):
        filter_value = search_entry.get().strip()

        volunteers_treeview.delete(*volunteers_treeview.get_children())

        self.volunteers = PersonDataRetrieve.get_volunteers(
            campID=camp.campID, name=filter_value
        )

        unique_volunteers = {v.volunteerID: v for v in self.volunteers}.values()

        if not unique_volunteers:
            volunteers_treeview.insert("", "end", text="No matching volunteers found.")
        else:
            for volunteer in unique_volunteers:
                volunteers_treeview.insert(
                    "",
                    "end",
                    text=volunteer.volunteerID,
                    values=(
                        f"{volunteer.first_name} {volunteer.last_name}",
                        volunteer.phone,
                    ),
                )

    def on_refugee_double_click(self, event, treeview):
        item = treeview.focus()
        if item:
            refugee_id = treeview.item(item, "text")

            selected_refugee_list = PersonDataRetrieve.get_refugees(id=refugee_id)
            if selected_refugee_list:
                selected_refugee = selected_refugee_list[0]
                self.show_screen("EditRefugee", selected_refugee)

    def on_volunteer_double_click(self, event, treeview):
        item = treeview.focus()
        if item:
            volunteer_id = treeview.item(item, "text")
            selected_volunteer_list = PersonDataRetrieve.get_volunteers(
                volunteerID=volunteer_id
            )
            if selected_volunteer_list:
                selected_volunteer = selected_volunteer_list[0]
                self.show_screen("EditVolunteer", selected_volunteer)


class VolunteerDashboard(Dashboard):
    """
    Takes in a volunteer object and displays a dashboard with information on that volunteer's camp.

    """

    def setup_dashboard(self, volunteer):
        self.camp = CampDataRetrieve.get_camp(campID=volunteer.campID)[0]
        self.plan = PlanDataRetrieve.get_plan(planID=self.camp.planID)[0]

        self.tab_control = ttk.Notebook(self)
        camp_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(camp_tab, text=f"Camp {self.camp.campID}")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_camp_tab(camp_tab, self.camp, self.plan, "volunteer")


class AdminDashboard(Dashboard):
    """
    Admin dashboard for displaying information on each camp and additional resources.2
    Includes an overview tab with information on all camps plus additional resources,
    as well as individual tabs for each camp, a resource distribution tab, and a statistics tab.
    """

    def setup_dashboard(self, plan):
        self.plan = plan

        self.planCamps = CampDataRetrieve.get_camp(planID=plan.planID)

        self.tab_control = ttk.Notebook(self)

        self.create_admin_tabs()

        self.tab_control.pack(expand=1, fill="both")

    def create_admin_tabs(self):
        self.setup_distribute_resources_tab()

        self.setup_plan_statistics_tab()

        self.setup_camp_tabs()

    def setup_camp_tabs(self):
        user_type = "admin"
        for camp in self.planCamps:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=f"Camp {camp.campID}")
            self.setup_camp_tab(tab, camp, self.plan, user_type)

    def setup_distribute_resources_tab(self):
        distribute_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(distribute_tab, text="Distribute Plan Resources")

        self.create_plan_tab_title(distribute_tab, self.plan)

        additional_resources_frame = self.create_additional_resources_section(
            distribute_tab, self.plan
        )

        canvas_width = 600
        camp_resources_canvas = tk.Canvas(distribute_tab, width=canvas_width)
        camp_resources_scrollbar = ttk.Scrollbar(
            distribute_tab, orient="horizontal", command=camp_resources_canvas.xview
        )
        camp_resources_canvas.configure(xscrollcommand=camp_resources_scrollbar.set)

        all_camp_resources_frame = ttk.Frame(camp_resources_canvas)
        camp_resources_canvas.create_window(
            (0, 1), window=all_camp_resources_frame, anchor="nw"
        )

        for i, camp in enumerate(self.planCamps):
            camp_title = f"Camp {camp.campID} - {camp.location}"
            camp_title_label = tk.Label(
                all_camp_resources_frame, text=camp_title, font=("Arial", 11, "bold")
            )
            camp_title_label.grid(row=0, column=i * 2, sticky="w")

            camp_section = self.create_resources_section(
                all_camp_resources_frame,
                camp,
                self.plan,
                "admin",
                additional_resources_frame=additional_resources_frame,
            )
            camp_section.grid(row=1, column=i * 2, sticky="nsew")
            all_camp_resources_frame.grid_columnconfigure(i * 2 + 1, weight=1)

        all_camp_resources_frame.bind(
            "<Configure>",
            lambda e: camp_resources_canvas.configure(
                scrollregion=camp_resources_canvas.bbox("all")
            ),
        )

        additional_resources_frame.grid(row=2, column=0, sticky="nsew")
        camp_resources_canvas.grid(row=2, column=1, sticky="nsew")
        camp_resources_scrollbar.grid(row=3, column=1, sticky="ew")
        distribute_tab.grid_columnconfigure(0, weight=1)
        distribute_tab.grid_columnconfigure(1, weight=3)

    def create_plan_tab_title(self, parent_tab, plan):
        title_frame = tk.Frame(parent_tab)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_frame.columnconfigure(0, weight=1)

        plan_name = f"Plan {plan.planID}: {plan.name} - {plan.country}"
        plan_description = plan.description

        title_label = tk.Label(title_frame, text=plan_name, font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        description_label = tk.Label(
            title_frame, text=plan_description, font=("Arial", 14)
        )
        description_label.grid(row=1, column=0, sticky="w", padx=5, pady=(0, 5))

        new_camp_button = ttk.Button(
            title_frame,
            text="New Camp",
            command=lambda: self.show_screen("NewCamp", plan),
        )
        new_camp_button.grid(row=0, column=1, pady=(5, 0))

        new_camp_item_button = ttk.Button(
            title_frame,
            text="Camp List",
            command=lambda: self.show_screen("CampList", plan),
        )
        new_camp_item_button.grid(row=0, column=2, pady=(5, 0))

        edit_button = ttk.Button(
            title_frame,
            text="Edit Plan",
            style="TButton",
            command=lambda: self.show_screen("EditPlan", plan),
        )
        edit_button.grid(row=0, column=3, padx=5, pady=(5, 0))

        title_frame.columnconfigure(1, weight=1)
        title_frame.columnconfigure(2, weight=1)
        title_frame.columnconfigure(3, weight=1)

        parent_tab.grid_rowconfigure(0, weight=0)
        parent_tab.grid_rowconfigure(1, weight=0)
        parent_tab.grid_rowconfigure(2, weight=1)

    def setup_plan_statistics_tab(self):
        stats_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(stats_tab, text="Plan Statistics")

        self.create_plan_tab_title(stats_tab, self.plan)

        additional_resources_frame = self.create_additional_resources_section(
            stats_tab, self.plan
        )

        canvas_width = 600
        camp_stats_canvas = tk.Canvas(stats_tab, width=canvas_width)
        camp_resources_scrollbar = ttk.Scrollbar(
            stats_tab, orient="horizontal", command=camp_stats_canvas.xview
        )
        camp_stats_canvas.configure(xscrollcommand=camp_resources_scrollbar.set)

        all_camp_stats_frame = ttk.Frame(camp_stats_canvas)
        camp_stats_canvas.create_window(
            (0, 1), window=all_camp_stats_frame, anchor="nw"
        )

        for i, camp in enumerate(self.planCamps):
            camp_title = f"Camp {camp.campID} - {camp.location}"
            camp_title_label = tk.Label(
                all_camp_stats_frame, text=camp_title, font=("Arial", 12, "bold")
            )
            camp_title_label.grid(row=0, column=i * 2, sticky="w")

            camp_stats = self.create_camp_statistics_section(all_camp_stats_frame, camp)
            camp_stats.grid(row=1, column=i * 2, sticky="nsew")
            all_camp_stats_frame.grid_columnconfigure(i * 2 + 1, weight=1)

        all_camp_stats_frame.bind(
            "<Configure>",
            lambda e: camp_stats_canvas.configure(
                scrollregion=camp_stats_canvas.bbox("all")
            ),
        )

        additional_resources_frame.grid(row=2, column=0, sticky="nsew")
        camp_stats_canvas.grid(row=2, column=1, sticky="nsew")
        camp_resources_scrollbar.grid(row=3, column=1, sticky="ew")
        stats_tab.grid_columnconfigure(0, weight=1)
        stats_tab.grid_columnconfigure(1, weight=3)
