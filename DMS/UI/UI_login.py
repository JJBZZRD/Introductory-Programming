import tkinter as tk
from ..Logic.person_data_retrieve import PersonDataRetrieve


class LoginScreen(tk.Frame):

    def login(self, username, password):

        print(username)
        print(password)
        res = PersonDataRetrieve.login(str(username), str(password))
        print(res)
        for r in res:
            print(r.display_info())

        if isinstance(res, str):
            self.error_label.config(text=res)
        elif len(res) != 1:
            self.error_label.config(text="Invalid credentials")
        else:
            self.set_user(res[0])
            if res[0].campID is None:
                screen = 'PlanList'
            else:
                screen = 'VolunteerDashboard'
            self.show_screen(screen, res[0])

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
        # password_entry = tk.Entry(self)
        password_entry = tk.Entry(self, show="*")
        password_entry.pack()

        password_entry.bind("<Return>", lambda event: self.login(username_entry.get(), password_entry.get()))

        login_button = tk.Button(self, text="Login", command= lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=5)

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

        # for person in PersonDataRetrieve.get_all_volunteers():
        #     print(person.display_info())



