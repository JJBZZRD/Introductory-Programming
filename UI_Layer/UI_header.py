import tkinter as tk
from tkinter import ttk
from UI_login import LoginScreen
import UI_modify_entries as me


class UIHeader(tk.Frame):
    def __init__(self, root, show_screen, page_nav, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.show_screen = show_screen
        self.page_nav = page_nav
        self.create_header()

    def logout(self):
        self.show_screen(LoginScreen)

    def navigate_back(self):
        self.page_nav('back')

    def navigate_forward(self):
        self.page_nav('forward')

    def open_settings(self):
        self.show_screen(me.EditVolunteer)

    '''@staticmethod
    def change_role(event=None):
        pass  # Placeholder for role change logic'''

    def create_header(self, header_name='camp_1'):
        header = tk.Frame(self, bg='white')

        # Logo on the left
        logo_label = tk.Label(header, text="LOGO", bg="white")
        logo_label.pack(side=tk.LEFT, padx=(10, 20))

        # Camp name
        camp_label = tk.Label(header, text=header_name, bg="white", font=("Helvetica", 16))
        camp_label.pack(side=tk.LEFT)

        # Spacer
        spacer = tk.Frame(header, bg='white')
        spacer.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Dropdown menu for roles
        '''role_menu = ttk.Combobox(header, values=["Admin", "User"], state="readonly")
        role_menu.set("Admin")  # set default value
        role_menu.pack(side=tk.LEFT)
        role_menu.bind('<<ComboboxSelected>>', UIHeader.change_role)'''

        # Navigation buttons
        nav_back_button = tk.Button(header, text="←", bg="white", command=self.navigate_back)
        nav_back_button.pack(side=tk.LEFT, padx=(10, 0))

        nav_forward_button = tk.Button(header, text="→", bg="white", command=self.navigate_forward)
        nav_forward_button.pack(side=tk.LEFT, padx=(0, 10))

        # Settings button
        settings_button = tk.Button(header, text="⚙", bg="white", command=self.open_settings)
        settings_button.pack(side=tk.LEFT)

        # Logout button
        logout_button = tk.Button(header, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT, padx=(0, 10))

        header.pack(side='top', fill='x')
