# app_ui.py

import tkinter as tk
from admin_interface import admin_dashboard
from volunteer_interface import volunteer_dashboard
from login_ui import show_login_screen

def main():
    root = tk.Tk()
    root.title("Refugee Support Application")
    show_login_screen(root)  # Start with the login screen
    root.mainloop()

if __name__ == "__main__":
    main()
