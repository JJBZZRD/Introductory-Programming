import tkinter as tk
from ..Logic.person_data_retrieve import PersonDataRetrieve
class LoginScreen(tk.Frame):
    def __init__(self, ui_manager, **kwargs):
        super().__init__(ui_manager.root, **kwargs)
        self.root = ui_manager.root
        self.show_screen = ui_manager.show_screen
        self.set_user = ui_manager.set_user
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
        
        for person in PersonDataRetrieve.get_all_volunteers():
            print(person.display_info())

    def on_login_as_admin_click(self):

        res = PersonDataRetrieve.login(self.username_entry, self.password_entry)

        if isinstance(res, str):
            # return invalid login message
            pass
        elif len(res) != 1:
            # return invalid login message
            pass 
        else:
            self.set_user(res[0])
            if res[0].campID is None:
                screen = 'PlanList'
            else:
                screen = 'VolunteerDashboard'
            self.show_screen(screen, res[0])
            
        


    def on_volunteer_login_click(self):
        self.set_user(volunteer1)
        self.show_screen('VolunteerDashboard', volunteer1)


