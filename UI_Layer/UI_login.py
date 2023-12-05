import tkinter as tk
#from UI_dashboard import AdminDashboard, VolunteerDashboard
#from UI_manage_list import PlanList


class LoginScreen(tk.Frame):
    def __init__(self, root, show_screen, set_user, *args, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.show_screen = show_screen
        self.set_user = set_user
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

        #admin_acount = admin()   this will be a an admin account object passed to the set_user method on succesfful login

        self.set_user(admin_account)
        self.show_screen('PlanList', 1)

    def on_volunteer_login_click(self):
        self.show_screen('VolunteerDashboard', 1) #placeholder for actual logic


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
