import tkinter as tk


class UIHeader(tk.Frame):
    def __init__(self, root, show_screen, page_nav, reset_history, logged_in_user, *args, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.logged_in_user = logged_in_user
        self.show_screen = show_screen
        self.page_nav = page_nav
        self.reset_history = reset_history
        self.create_header()

    def create_header(self):
        header = tk.Frame(self, bg='white')

        logo_label = tk.Label(header, text="LOGO", bg="white", font=("Arial", 16))
        logo_label.pack(side=tk.LEFT, padx=(10, 20))

        # logged_in_user is a user object and .name provides the username
        camp_label = tk.Label(header, text="Logged in as: " + self.logged_in_user.Fname, bg="white",
                              font=("Helvetica", 16))  #
        camp_label.pack(side=tk.LEFT)

        spacer = tk.Frame(header, bg='white')
        spacer.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.add_navigation_buttons(header)
        self.add_control_buttons(header)

        header.pack(side='top', fill='x')

    def add_navigation_buttons(self, parent):
        nav_back_button = tk.Button(parent, text="←", bg="white",
                                    command=lambda: self.page_nav('back'))
        nav_back_button.pack(side=tk.LEFT, padx=(10, 0))

        nav_forward_button = tk.Button(parent, text="→", bg="white",
                                       command=lambda: self.page_nav('forward'))
        nav_forward_button.pack(side=tk.LEFT, padx=(0, 10))

    def add_control_buttons(self, parent):
        settings_button = tk.Button(parent, text="⚙", bg="white", command=self.open_settings)
        settings_button.pack(side=tk.LEFT)

        logout_button = tk.Button(parent, text="Logout", bg="white", command=self.logout)
        logout_button.pack(side=tk.RIGHT, padx=(0, 10))

    def logout(self):
        self.show_screen('LoginScreen')
        self.reset_history()

    def open_settings(self):
        self.show_screen('EditVolunteer', self.logged_in_user)
