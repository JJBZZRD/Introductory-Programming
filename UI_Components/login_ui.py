# login_ui.py

import tkinter as tk
from admin_interface.admin_dashboard import show_admin_dashboard
from volunteer_interface.volunteer_dashboard import show_volunteer_dashboard

def show_login_screen(root):
    def login_as_admin():
        # This will eventually hold logic for admin login
        show_admin_dashboard(root)

    def login_as_volunteer():
        # This will eventually hold logic for volunteer login
        show_volunteer_dashboard(root)

    # Create a frame to hold the login fields and buttons
    login_frame = tk.Frame(root)
    login_frame.pack(pady=20)

    # Username field
    tk.Label(login_frame, text="Username:").pack()
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    # Password field
    tk.Label(login_frame, text="Password:").pack()
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.pack()

    # Login button for the admin
    admin_login_button = tk.Button(login_frame, text="Admin Login", command=login_as_admin)
    admin_login_button.pack(pady=5)

    # Login button for the volunteer
    volunteer_login_button = tk.Button(login_frame, text="Volunteer Login", command=login_as_volunteer)
    volunteer_login_button.pack(pady=5)

# The following would be in your main app file where you initialize the root Tk instance
# and call show_login_screen to display the login GUI.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login")
    show_login_screen(root)
    root.mainloop()
