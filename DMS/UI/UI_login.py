import tkinter as tk
from tkinter import PhotoImage
from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..Logic.plan_data_retrieve import PlanDataRetrieve
from ..Logic.camp_data_retrieve import CampDataRetrieve
import os
import sys

class LoginScreen(tk.Frame):
    def login(self, username, password):
        print(username)
        print(password)
        res = PersonDataRetrieve.login(str(username), str(password))
        print(res)
        for r in res:
            print(r.display_info())


        if len(res) > 0 and res[0].account_status == 'Inactive':
            self.error_label.config(text="Your account has been deactivated, contact the administrator")
        elif isinstance(res, str):
            self.error_label.config(text=res)
        elif len(res) != 1:
            self.error_label.config(text="Invalid credentials")
        else:
            self.set_user(res[0])
            if res[0].campID is None:
                screen = "PlanList"
                self.show_screen(screen, res[0])
            else:
                # screen = "VolunteerDashboard"
                screen = "AdminDashboard"
                camp = CampDataRetrieve.get_camp(campID=res[0].campID)
                plan = PlanDataRetrieve.get_plan(planID=camp[0].planID)
                self.show_screen(screen, plan[0])

    def __init__(self, ui_manager, **kwargs):
        super().__init__(ui_manager.root, **kwargs)
        self.root = ui_manager.root
        self.show_screen = ui_manager.show_screen
        self.set_user = ui_manager.set_user
        self.setup_login_screen()

    def setup_login_screen(self):
        login_frame = tk.Frame(self)
        login_frame.pack(padx=10, pady=10)

        original_image = PhotoImage(file="DMS/UI/logo.png")
        logo_label = tk.Label(login_frame, image=original_image)
        logo_label.image = original_image
        logo_label.grid(row=0, column=0, columnspan=2, padx=(10, 20), pady=(10, 20))

        tk.Label(login_frame, text="Username:").grid(
            row=1, column=0, sticky="ew", padx=5, pady=5
        )
        username_entry = tk.Entry(login_frame)
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(login_frame, text="Password:").grid(
            row=2, column=0, sticky="ew", padx=5, pady=5
        )
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        password_entry.bind(
            "<Return>",
            lambda event: self.login(username_entry.get(), password_entry.get()),
        )

        login_button = tk.Button(
            login_frame,
            text="Login",
            command=lambda: self.login(username_entry.get(), password_entry.get()),
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.error_label = tk.Label(login_frame, text="", fg="red")
        self.error_label.grid(row=4, column=0, columnspan=2)

        username_entry.focus_set()
