import tkinter as tk
from tkinter import messagebox
# Import the AuthenticationService class from the BusinessLogicLayer package
from BusinessLogicLayer.authentication_service import AuthenticationService
# Import the Dashboard classes from the PresentationLayer package
from PresentationLayer.dashboard_admin import AdminDashboard
from PresentationLayer.dashboard_volunteer import VolunteerDashboard

class LoginInterface(tk.Frame):
    """
    LoginInterface is a class that creates a login form as a Tkinter Frame.
    It inherits from tk.Frame and contains input fields for username and password,
    and a button to submit the credentials for authentication.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Constructor for the LoginInterface class.
        This method initializes the Frame, adds labels, entry widgets for username and password,
        and a button to trigger the authentication process.

        :param parent: The parent widget, typically a Tkinter window, to attach this Frame to.
        """
        super().__init__(parent, *args, **kwargs)

        # Create and pack the 'Username' label and entry widget
        self.label_username = tk.Label(self, text="Username")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        # Create and pack the 'Password' label and entry widget
        self.label_password = tk.Label(self, text="Password")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        # Create and pack the 'Login' button
        self.button_login = tk.Button(self, text="Login", command=self.authenticate_user)
        self.button_login.pack()

    def authenticate_user(self):
        """
        This method is called when the user clicks the 'Login' button.
        It retrieves the entered username and password, and uses the AuthenticationService
        to validate the credentials. Depending on the validation result, it either shows
        an error or switches to the appropriate dashboard.
        """
        # Retrieve entered username and password
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Use the AuthenticationService to validate the credentials
        if AuthenticationService.authenticate(username, password):
            # Display a success message
            messagebox.showinfo("Login Success", "Successfully logged in!")

            # Determine which dashboard to open based on the username
            if username == "admin":
                # Switch to AdminDashboard
                self.master.switch_to_dashboard(AdminDashboard)
            else:
                # Switch to VolunteerDashboard
                self.master.switch_to_dashboard(VolunteerDashboard)
        else:
            # Display an error message for failed authentication
            messagebox.showerror("Login Failed", "Incorrect username or password")
