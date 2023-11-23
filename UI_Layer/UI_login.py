import tkinter as tk
from UI_dashboard import AdminDashboard, VolunteerDashboard

class LoginScreen(tk.Frame):
    def __init__(self, parent, callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.callback = callback
        self.setup_login_screen()

    def setup_login_screen(self):
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        admin_login_button = tk.Button(self, text="Admin Login", command=self.login_as_admin)
        admin_login_button.pack(pady=5)

        volunteer_login_button = tk.Button(self, text="Volunteer Login", command=self.login_as_volunteer)
        volunteer_login_button.pack(pady=5)


    def login_as_admin(self):
        # Use the callback to transition to the Admin Plans screen
        self.callback(AdminDashboard)
        self.clear()

    def login_as_volunteer(self):
        # Use the callback to transition to the Volunteer Dashboard
        self.callback(VolunteerDashboard)
        self.clear()

    def clear(self):
        self.destroy()
