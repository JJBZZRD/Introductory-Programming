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
        self.ui_manager = ui_manager

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
        title_frame = tk.Frame(parent_tab, relief="solid", borderwidth=2)
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        title_frame.columnconfigure(0, weight=2)
        title_frame.columnconfigure(1, weight=0)
        title_frame.columnconfigure(2, weight=0)

        camp_title_text = f"Camp {camp.campID} - {camp.location}"
        camp_title_label = tk.Label(
            title_frame, text=camp_title_text, font=("Arial", 16, "bold")
        )
        camp_title_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        plan_title_text = f"Plan {plan.planID}: {plan.name} - {plan.country}"
        plan_title_label = tk.Label(
            title_frame, text=plan_title_text, font=("Arial", 14)
        )
        plan_title_label.grid(row=1, column=0, sticky="w", padx=5, pady=(0, 5))

        edit_camp_button = ttk.Button(
            title_frame,
            text="Edit Camp",
            command=lambda: self.show_screen("EditCamp", camp),
        )
        edit_camp_button.grid(
            row=0, column=2, rowspan=2, sticky="e", padx=(5, 15), pady=5
        )

        parent_tab.grid_rowconfigure(0, weight=0)
        parent_tab.grid_rowconfigure(1, weight=1)

    def create_camp_statistics_section(self, parent_tab, camp):
        camp_statistics_frame = tk.Frame(parent_tab, relief="solid", borderwidth=2)
        camp_statistics_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

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

        separate_families = (
            family_stats.get("separate_families", "Error fetching separate families")
            if isinstance(family_stats, dict)
            else family_stats
        )

        num_separate_families = len(separate_families)

        stats_functions = [
            ("Gender Distribution", gender_stats),
            ("Age Distribution", age_stats),
            ("Vital Status", vital_status_stats),
            ("Triage Categories", triage_stats),
        ]

        row = 0

        tk.Label(
            camp_statistics_frame,
            text=f"{camp.location} Camp Statistics",
            font=("Arial", 14, "bold"),
        ).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        row += 1

        separator = tk.ttk.Separator(camp_statistics_frame, orient="horizontal")
        separator.grid(row=row, column=0, columnspan=5, sticky="ew", pady=5)
        row += 1

        tk.Label(
            camp_statistics_frame,
            text=f"Volunteers: {num_volunteers}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            camp_statistics_frame,
            text=f"Refugees: {num_refugees}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            camp_statistics_frame,
            text=f"Number of Families: {num_families}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            camp_statistics_frame,
            text=f"Number of Separated Families: {num_separate_families}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            camp_statistics_frame,
            text=f"IDs of Separated Families: {str(separate_families)[1:-1]}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        for label, stats in stats_functions:
            separator = tk.ttk.Separator(camp_statistics_frame, orient="horizontal")
            separator.grid(row=row, column=0, columnspan=5, sticky="ew", pady=5)
            row += 1

            tk.Label(
                camp_statistics_frame,
                text=label,
            ).grid(row=row, column=0, sticky="w", padx=5)
            row += 1

            if isinstance(stats, str):
                tk.Label(
                    camp_statistics_frame,
                    text=stats,
                ).grid(row=row, column=0, sticky="w", padx=5)
                row += 1
                continue

            stats_text = ""
            for key, value in stats.items():
                if "num_" in key:
                    key_parts = key.split("_", 1)  # Split only at the first underscore
                    pct_key = "pct_" + key_parts[1]
                    pct_value = stats.get(pct_key, 0)
                    formatted_key = key_parts[1].replace('_', ' ').title()  # Replace subsequent underscores with spaces
                    formatted_stat = (
                        f"{formatted_key}: {pct_value:.0f}% ({value})"
                    )
                    stats_text += formatted_stat + " | "
            
            stats_text = stats_text.rstrip(" | ")

            tk.Label(
                camp_statistics_frame,
                text=stats_text,
            ).grid(row=row, column=0, sticky="w", padx=5)
            row += 1

        return camp_statistics_frame

    def create_resources_section(self, parent_tab, camp, plan, user_type):
        resources_frame = tk.Frame(parent_tab, relief="solid", borderwidth=2)
        resources_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        resources_frame.grid_columnconfigure(1, weight=1)

        title_label = tk.Label(
            resources_frame,
            text=f"Current Resources in {camp.location}",
            font=("Arial", 14, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=5, sticky="w", padx=5, pady=5)

        camp_resources_estimation = CampDataRetrieve.get_camp_resources(camp.campID)

        resources = {
            "Shelter": camp.shelter,
            "Water": camp.water,
            "Food": camp.food,
            "Medical Supplies": camp.medical_supplies,
        }

        for index, (resource_name, amount) in enumerate(resources.items()):
            resource_row = index * 3 + 1

            separator = tk.ttk.Separator(resources_frame, orient="horizontal")
            separator.grid(
                row=resource_row, column=0, columnspan=5, sticky="ew", pady=5
            )

            tk.Label(resources_frame, text=f"{resource_name}: {amount}").grid(
                row=resource_row + 1, column=0, sticky="w", padx=5, pady=5
            )

            match resource_name:
                case "Shelter":
                    plan_resouce = "shelter"
                case "Water":
                    plan_resouce = "water"
                case "Food":
                    plan_resouce = "food"
                case "Medical Supplies":
                    plan_resouce = "medical_supplies"

            amount = 0 if isinstance(amount, str) else amount
            if amount > 0:
                tk.Button(
                    resources_frame,
                    text="-10",
                    command=lambda res_name=resource_name: self.update_resource(
                        camp,
                        resources_frame,
                        res_name,
                        -10,
                        plan,
                        user_type,
                    ),
                ).grid(row=resource_row + 1, rowspan=2, column=2, padx=5)

            if (
                user_type == "admin" and getattr(plan, plan_resouce) > 0
            ) or user_type == "volunteer":
                tk.Button(
                    resources_frame,
                    text="+10",
                    command=lambda res_name=resource_name: self.update_resource(
                        camp,
                        resources_frame,
                        res_name,
                        10,
                        plan,
                        user_type,
                    ),
                ).grid(row=resource_row + 1, rowspan=2, column=3, padx=5)

            if resource_name == "Shelter":
                num_refugees = len(PersonDataRetrieve.get_refugees(camp_id=camp.campID))

                shelter_colour = "red" if num_refugees > camp.shelter else "black"

                tk.Label(
                    resources_frame,
                    text=f"Camp refugees: {int(num_refugees)}",
                    fg=shelter_colour,
                ).grid(
                    row=resource_row + 2,
                    column=0,
                    columnspan=5,
                    sticky="w",
                    padx=5,
                    pady=5,
                )

            if resource_name in ["Water", "Food", "Medical Supplies"]:
                days_left = camp_resources_estimation.get(resource_name)

                days_left_color = "red" if days_left < 7 else "black"

                tk.Label(
                    resources_frame,
                    text=f"Estimated days left: {int(days_left)}",
                    fg=days_left_color,
                ).grid(
                    row=resource_row + 2,
                    column=0,
                    columnspan=5,
                    sticky="w",
                    padx=5,
                    pady=5,
                )

            self.rebuild_additional_resources_frame(plan)
        return resources_frame

    def rebuild_resources_frame(self, camp, resource_frame, plan, user_type):
        parent_tab = resource_frame.master
        resource_frame.destroy()

        new_resources_frame = self.create_resources_section(
            parent_tab, camp, plan, user_type
        )
        new_resources_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def rebuild_additional_resources_frame(self, plan):
        self.additional_resources_frame.destroy()

        self.additional_resources_frame = self.create_additional_resources_section(
            self.additional_resources_frame.master, plan
        )
        self.additional_resources_frame.grid(
            row=1, column=0, sticky="nsew", padx=5, pady=5
        )

    def update_resource(
        self,
        camp,
        resource_frame,
        resource_name,
        increment,
        plan,
        user_type,
    ):
        resource_key = resource_name.lower().replace(" ", "_")
        if user_type == "admin":
            plan_current_amount = getattr(plan, resource_key)
            new_plan_amount = max(0, plan_current_amount - increment)
            if PlanEdit.update_plan(plan.planID, **{resource_key: new_plan_amount}):
                setattr(plan, resource_key, new_plan_amount)

        camp_current_amount = getattr(camp, resource_key)
        new_camp_amount = max(0, camp_current_amount + increment)
        if CampDataEdit.update_camp(camp.campID, **{resource_key: new_camp_amount}):
            setattr(camp, resource_key, new_camp_amount)

        aaa = "canvas" in str(resource_frame.master)
        # print(f"Parent tab: {resource_frame.master}")
        # print(f" {aaa}")
        if aaa:
            try:
                self.ui_manager.refresh_page()
            except:
                pass
        else:
            self.rebuild_resources_frame(camp, resource_frame, plan, user_type)

        # if user_type == "admin":
        #     self.ui_manager.refresh_page()
        # self.rebuild_additional_resources_frame(plan)

    def create_additional_resources_section(self, parent_frame, plan):
        additional_resources_frame = tk.Frame(
            parent_frame, relief="solid", borderwidth=2
        )
        additional_resources_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        additional_resources_frame.grid_columnconfigure(1, weight=1)

        title_label = tk.Label(
            additional_resources_frame,
            text=f"Plan {plan.planID} Undistributed Resources",
            font=("Arial", 14, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        additional_resources = {
            "Shelter": plan.shelter,
            "Water": plan.water,
            "Food": plan.food,
            "Medical Supplies": plan.medical_supplies,
        }

        for index, (resource_name, amount) in enumerate(additional_resources.items()):
            resource_row = index * 2 + 1

            separator = tk.ttk.Separator(
                additional_resources_frame, orient="horizontal"
            )
            separator.grid(
                row=resource_row, column=0, columnspan=3, sticky="ew", pady=5
            )

            tk.Label(
                additional_resources_frame, text=f"{resource_name}: {amount}"
            ).grid(row=resource_row + 1, column=0, sticky="w", padx=5)

            amount = 0 if isinstance(amount, str) else amount
            if amount > 0:
                tk.Button(
                    additional_resources_frame,
                    text="-10",
                    command=lambda res_name=resource_name: self.update_plan_resources(
                        additional_resources_frame,
                        res_name,
                        plan,
                        -10,
                    ),
                ).grid(row=resource_row + 1, column=1, padx=5, sticky="e")

            tk.Button(
                additional_resources_frame,
                text="+10",
                command=lambda res_name=resource_name: self.update_plan_resources(
                    additional_resources_frame,
                    res_name,
                    plan,
                    10,
                ),
            ).grid(row=resource_row + 1, column=2, padx=5)

        tk.Label(
            additional_resources_frame,
            text=f"\nButtons above update plan {plan.planID}'s available nadditional resources.",
        ).grid(
            row=len(additional_resources) * 2 + 2,
            column=0,
            columnspan=3,
            sticky="w",
            padx=5,
            pady=5,
        )

        tk.Label(
            additional_resources_frame,
            text=f"\nButtons under camp headings distribute plan {plan.planID}'s additional resources.",
        ).grid(
            row=len(additional_resources) * 2 + 3,
            column=0,
            columnspan=3,
            sticky="w",
            padx=5,
            pady=5,
        )

        return additional_resources_frame

    def update_plan_resources(self, resource_frame, resource_name, plan, increment):
        resource_key = resource_name.lower().replace(" ", "_")
        current_amount = getattr(plan, resource_key)
        new_amount = max(0, current_amount + increment)

        if PlanEdit.update_plan(plan.planID, **{resource_key: new_amount}):
            setattr(plan, resource_key, new_amount)

        self.ui_manager.refresh_page()

    def create_camp_refugees_volunteers_section(
        self, parent_tab, camp, display_type, user_type
    ):
        refugees_volunteers_frame = tk.Frame(parent_tab, relief="solid", borderwidth=2)
        refugees_volunteers_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

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
        refugees_title.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        if user_type == "admin":
            switch_text = (
                "Switch to Volunteers"
                if display_type == "refugees"
                else "Switch to Refugees"
            )
            switch_button = tk.Button(
                refugees_volunteers_frame,
                text=switch_text,
                command=lambda: self.create_camp_refugees_volunteers_section(
                    parent_tab,
                    camp,
                    "volunteers" if display_type == "refugees" else "refugees",
                    user_type,
                ),
            )
            switch_button.grid(row=0, column=0, sticky="e", padx=5)

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
            text="Search by name",
            command=lambda: update_list_func(camp, search_entry, refugees_treeview),
        )
        filter_button.grid(row=0, column=1, padx=3)

        update_list_func(camp, search_entry, refugees_treeview)

        manage_button = ttk.Button(
            refugees_volunteers_frame,
            text=f"Manage Camp {display_type.capitalize()}",
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
        refugees_treeview.column("#0", width=40, anchor="center")
        refugees_treeview.column("#1", anchor="center")
        refugees_treeview.column("#2", anchor="center")

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
        volunteers_treeview.column("#0", width=40)
        volunteers_treeview.column("#1", anchor="center")
        volunteers_treeview.column("#2", anchor="center")

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
    Displays a dashboard with information on that volunteer's camp.

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
    Displays information on each camp in plan and adds a plan resource distribution and statistics tabs.
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
        self.additional_resources_frame = self.create_additional_resources_section(
            distribute_tab, self.plan
        )

        (
            camp_resources_canvas,
            camp_resources_scrollbar,
            _,
        ) = self.create_camp_resources_section(distribute_tab)

        self.additional_resources_frame.grid(
            row=1, column=0, sticky="nsew", padx=5, pady=5
        )
        camp_resources_canvas.grid(row=1, column=1, sticky="nsew", padx=5)
        camp_resources_scrollbar.grid(row=2, column=1, sticky="ew", padx=5)

        distribute_tab.grid_columnconfigure(0, weight=1)
        distribute_tab.grid_columnconfigure(1, weight=3)
        distribute_tab.grid_rowconfigure(1, weight=1)

    def setup_plan_statistics_tab(self):
        stats_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(stats_tab, text="Plan Statistics")

        self.create_plan_tab_title(stats_tab, self.plan)
        plan_stats_section = self.create_plan_statistics_section(stats_tab, self.plan)

        (
            camp_stats_canvas,
            camp_stats_scrollbar,
            _,
        ) = self.create_all_camp_statistics_section(stats_tab)

        plan_stats_section.grid(row=1, column=0, sticky="nsew", padx=5)
        camp_stats_canvas.grid(row=1, column=1, sticky="nsew", padx=5)
        camp_stats_scrollbar.grid(row=2, column=1, sticky="ew", padx=5)

        stats_tab.grid_columnconfigure(0, weight=1)
        stats_tab.grid_columnconfigure(1, weight=3)
        stats_tab.grid_rowconfigure(1, weight=1)

    def create_camp_resources_section(self, parent):
        canvas_width = 450
        camp_resources_canvas = tk.Canvas(parent, width=canvas_width)
        camp_resources_scrollbar = ttk.Scrollbar(
            parent, orient="horizontal", command=camp_resources_canvas.xview
        )
        camp_resources_canvas.configure(xscrollcommand=camp_resources_scrollbar.set)

        all_camp_resources_frame = ttk.Frame(camp_resources_canvas)
        camp_resources_canvas.create_window(
            (0, 0), window=all_camp_resources_frame, anchor="nw"
        )

        for i, camp in enumerate(self.planCamps):
            self.populate_all_camp_resources(all_camp_resources_frame, camp, i)

        all_camp_resources_frame.bind(
            "<Configure>",
            lambda e: camp_resources_canvas.configure(
                scrollregion=camp_resources_canvas.bbox("all")
            ),
        )

        return camp_resources_canvas, camp_resources_scrollbar, all_camp_resources_frame

    def populate_all_camp_resources(self, parent_frame, camp, column_index):
        camp_section = self.create_resources_section(
            parent_frame,
            camp,
            self.plan,
            "admin",
        )
        camp_section.grid(row=1, column=column_index * 2, sticky="nsew")
        parent_frame.grid_columnconfigure(column_index * 2 + 1, weight=1)

    def create_all_camp_statistics_section(self, parent):
        canvas_width = 450
        camp_stats_canvas = tk.Canvas(parent, width=canvas_width)
        camp_stats_scrollbar = ttk.Scrollbar(
            parent, orient="horizontal", command=camp_stats_canvas.xview
        )
        camp_stats_canvas.configure(xscrollcommand=camp_stats_scrollbar.set)

        all_camp_stats_frame = ttk.Frame(camp_stats_canvas)
        camp_stats_canvas.create_window(
            (0, 0), window=all_camp_stats_frame, anchor="nw"
        )

        for i, camp in enumerate(self.planCamps):
            self.populate_camp_statistics(all_camp_stats_frame, camp, i)

        all_camp_stats_frame.bind(
            "<Configure>",
            lambda e: camp_stats_canvas.configure(
                scrollregion=camp_stats_canvas.bbox("all")
            ),
        )

        return camp_stats_canvas, camp_stats_scrollbar, all_camp_stats_frame

    def populate_camp_statistics(self, parent_frame, camp, column_index):
        camp_stats = self.create_camp_statistics_section(parent_frame, camp)
        camp_stats.grid(row=1, column=column_index * 2, sticky="nsew")
        parent_frame.grid_columnconfigure(column_index * 2 + 1, weight=1)

    def create_plan_statistics_section(self, parent_tab, plan):
        plan_statistics_frame = tk.Frame(parent_tab, relief="solid", borderwidth=2)
        plan_statistics_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        planID = plan.planID
        triage_stats = PlanDataRetrieve.get_stats_triage_category(planID)
        gender_stats = PlanDataRetrieve.get_stats_gender(planID)
        age_stats = PlanDataRetrieve.get_stats_age(planID)
        vital_status_stats = PlanDataRetrieve.get_stats_vital_status(planID)

        num_volunteers = len(PersonDataRetrieve.get_volunteers_by_plan(planID))
        num_refugees = len(PersonDataRetrieve.get_refugees_by_plan(planID))
        family_stats = PlanDataRetrieve.get_stats_family(planID)
        num_families = (
            family_stats.get("num_families", "Error fetching families")
            if isinstance(family_stats, dict)
            else family_stats
        )

        separate_families = (
            family_stats.get("separate_families", "Error fetching families")
            if isinstance(family_stats, dict)
            else family_stats
        )

        num_separate_families = len(separate_families)

        stats_functions = [
            ("Gender Distribution", gender_stats),
            ("Age Distribution", age_stats),
            ("Vital Status", vital_status_stats),
            ("Triage Categories", triage_stats),
        ]

        row = 0

        tk.Label(
            plan_statistics_frame,
            text=f"{plan.name} Statistics",
            font=("Arial", 14, "bold"),
        ).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        row += 1

        separator = tk.ttk.Separator(plan_statistics_frame, orient="horizontal")
        separator.grid(row=row, column=0, columnspan=5, sticky="ew", pady=5)
        row += 1

        tk.Label(
            plan_statistics_frame,
            text=f"Volunteers: {num_volunteers}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            plan_statistics_frame,
            text=f"Refugees: {num_refugees}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            plan_statistics_frame,
            text=f"Number of Families: {num_families}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            plan_statistics_frame,
            text=f"Number of Separated Families: {num_separate_families}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        tk.Label(
            plan_statistics_frame,
            text=f"IDs of Separated Families: {str(separate_families)[1:-1]}",
        ).grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        for label, stats in stats_functions:
            separator = tk.ttk.Separator(plan_statistics_frame, orient="horizontal")
            separator.grid(row=row, column=0, columnspan=5, sticky="ew", pady=5)
            row += 1

            tk.Label(
                plan_statistics_frame,
                text=label,
            ).grid(row=row, column=0, sticky="w", padx=5)
            row += 1

            if isinstance(stats, str):
                tk.Label(
                    plan_statistics_frame,
                    text=stats,
                ).grid(row=row, column=0, sticky="w", padx=5)
                row += 1
                continue

            stats_text = ""
            for key, value in stats.items():
                if "num_" in key:
                    key_parts = key.split("_", 1)  # Split only at the first underscore
                    pct_key = "pct_" + key_parts[1]
                    pct_value = stats.get(pct_key, 0)
                    formatted_key = key_parts[1].replace('_', ' ').title()  # Replace subsequent underscores with spaces
                    formatted_stat = (
                        f"{formatted_key}: {pct_value:.0f}% ({value})"
                    )
                    stats_text += formatted_stat + " | "
            
            stats_text = stats_text.rstrip(" | ")

            tk.Label(
                plan_statistics_frame,
                text=stats_text,
            ).grid(row=row, column=0, sticky="w", padx=5)
            row += 1

        return plan_statistics_frame

    def create_plan_tab_title(self, parent_tab, plan):
        title_frame = tk.Frame(parent_tab, relief="solid", borderwidth=2)
        title_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        title_frame.columnconfigure(0, weight=2)
        title_frame.columnconfigure(1, weight=0)
        title_frame.columnconfigure(2, weight=0)
        title_frame.columnconfigure(3, weight=0)

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
        new_camp_button.grid(row=0, column=1, rowspan=2, padx=5)

        new_camp_item_button = ttk.Button(
            title_frame,
            text="Camp List",
            command=lambda: self.show_screen("CampList", plan),
        )
        new_camp_item_button.grid(row=0, column=2, rowspan=2, padx=5)

        edit_button = ttk.Button(
            title_frame,
            text="Edit Plan",
            style="TButton",
            command=lambda: self.show_screen("EditPlan", plan),
        )
        edit_button.grid(row=0, column=3, rowspan=2, padx=(5, 15))
