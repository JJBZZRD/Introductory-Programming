import tkinter as tk
#from UI_dashboard import AdminDashboard, VolunteerDashboard
#from UI_manage_list import PlanList
from dummydata import admin
from dummydata import volunteer1


class LoginScreen(tk.Frame):
    def __init__(self, root, show_screen, screen_data=None):
        super().__init__(root)
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

        admin_login_button = tk.Button(self, text="Admin Login", command=self.on_login_as_admin_click) #to be replaced with one button
        admin_login_button.pack(pady=5)

        volunteer_login_button = tk.Button(self, text="Volunteer Login", command=self.on_volunteer_login_click)
        volunteer_login_button.pack(pady=5)

    def on_login_as_admin_click(self):
        self.show_screen('PlanList', admin, add_to_history=False)


    def on_volunteer_login_click(self):
        self.show_screen('VolunteerDashboard', volunteer1, add_to_history=False)


        # placeholder validationt/login logic"
        # loginAttempt = logic.login()

        # if loginAttempt == False:
        #     message_popup('Invalid userid or password')
        # else:
        #     user = loginAttempt
        #     if user.type == 'volunteer':
        #         self.show_screen('volunteerDashboard', user.id)
        #     if user.type == 'admin
        #         self.show_screen('volunteerDashboard', user.id)
