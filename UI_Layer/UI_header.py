import tkinter as tk
from tkinter import ttk

class UIHeader:
    @staticmethod
    def logout():
        pass  # Placeholder for the logout logic

    @staticmethod
    def navigate_back():
        pass  # Placeholder for navigation logic

    @staticmethod
    def navigate_forward():
        pass

    @staticmethod
    def open_settings():
        pass  # Placeholder for settings logic

    @staticmethod
    def change_role(event=None):
        pass  # Placeholder for role change logic

    @staticmethod
    def create_header(parent):
        header = tk.Frame(parent, bg='white')

        # Logo on the left
        logo_label = tk.Label(header, text="LOGO", bg="white")
        logo_label.pack(side=tk.LEFT, padx=(10, 20))

        # Camp name
        camp_label = tk.Label(header, text="CAMP 1", bg="white", font=("Helvetica", 16))
        camp_label.pack(side=tk.LEFT)

        # Spacer
        spacer = tk.Frame(header, bg='white')
        spacer.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Dropdown menu for roles
        role_menu = ttk.Combobox(header, values=["Admin", "User"], state="readonly")
        role_menu.set("Admin")  # set default value
        role_menu.pack(side=tk.LEFT)
        role_menu.bind('<<ComboboxSelected>>', UIHeader.change_role)

        # Navigation buttons
        nav_back_button = tk.Button(header, text="←", bg="white", command=UIHeader.navigate_back)
        nav_back_button.pack(side=tk.LEFT, padx=(10, 0))

        nav_forward_button = tk.Button(header, text="→", bg="white", command=UIHeader.navigate_forward)
        nav_forward_button.pack(side=tk.LEFT, padx=(0, 10))

        # Settings button
        settings_button = tk.Button(header, text="⚙", bg="white", command=UIHeader.open_settings)
        settings_button.pack(side=tk.LEFT)

        # Logout button
        logout_button = tk.Button(header, text="Logout", command=UIHeader.logout)
        logout_button.pack(side=tk.RIGHT, padx=(0, 10))

        return header
