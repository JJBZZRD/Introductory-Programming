import tkinter as tk
from UI_dashboard import AdminDashboard, VolunteerDashboard
from UI_manage_list import PlanList


class LoginScreen(tk.Frame):
    def __init__(self, root, show_screen, *args, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.show_screen = show_screen
        self.setup_login_screen()

    def setup_login_screen(self):
        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self)
        username_entry.pack()

        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show="*")
        password_entry.pack()

        admin_login_button = tk.Button(self, text="Admin Login", command=self.login_as_admin)
        admin_login_button.pack(pady=5)

        volunteer_login_button = tk.Button(self, text="Volunteer Login", command=self.login_as_volunteer)
        volunteer_login_button.pack(pady=5)

    def login_as_admin(self):
        self.show_screen(PlanList)
        self.clear()

    def login_as_volunteer(self):
        self.show_screen(VolunteerDashboard)
        self.clear()

    def clear(self):
        self.destroy()
