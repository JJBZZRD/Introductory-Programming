# header_ui.py

import tkinter as tk
from tkinter import ttk

# Placeholder for the logout logic
def logout():
    pass

# Placeholder for navigation logic
def navigate_back():
    pass

def navigate_forward():
    pass

# Placeholder for settings logic
def open_settings():
    pass

# Placeholder for role change logic
def change_role(event=None):
    pass

def create_header(parent):
    header = tk.Frame(parent, bg='white')

    # Logo on the left
    logo_label = tk.Label(header, text="LOGO", bg="white")
    logo_label.pack(side=tk.LEFT, padx=(10, 20))

    # Camp name
    camp_label = tk.Label(header, text="CAMP 1", bg="white", font=("Helvetica", 16))
    camp_label.pack(side=tk.LEFT)

    # Spacer to push the rest to the right
    spacer = tk.Frame(header, bg='white')
    spacer.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Dropdown menu for roles - placeholder functionality
    role_menu = ttk.Combobox(header, values=["Admin", "User"], state="readonly")
    role_menu.set("Admin")  # set default value
    role_menu.pack(side=tk.LEFT)
    role_menu.bind('<<ComboboxSelected>>', change_role)

    # Navigation back button with placeholder functionality
    nav_back_button = tk.Button(header, text="←", bg="white", command=navigate_back)
    nav_back_button.pack(side=tk.LEFT, padx=(10, 0))

    # Navigation forward button with placeholder functionality
    nav_forward_button = tk.Button(header, text="→", bg="white", command=navigate_forward)
    nav_forward_button.pack(side=tk.LEFT, padx=(0, 10))

    # Settings button with placeholder functionality
    settings_button = tk.Button(header, text="⚙", bg="white", command=open_settings)
    settings_button.pack(side=tk.LEFT)

    # Logout button with placeholder functionality
    logout_button = tk.Button(header, text="Logout", command=logout)
    logout_button.pack(side=tk.RIGHT, padx=(0, 10))

    return header
