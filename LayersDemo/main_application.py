import tkinter as tk
# Import the LoginInterface class from the login_interface module in the PresentationLayer package
from PresentationLayer.login_interface import LoginInterface

class MainApplication(tk.Tk):
    """
    MainApplication is the main class for the Refugee Management System application.
    It inherits from tk.Tk which is the main class in Tkinter for creating a window.
    """

    def __init__(self, *args, **kwargs):
        """
        The constructor of the MainApplication class.
        Here, we initialize the main window with a title and a set geometry (size).
        We also create and display the LoginInterface within this window.
        """
        super().__init__(*args, **kwargs)

        # Set the title of the main window
        self.title("Refugee Management System")

        # Set the size of the window (width x height)
        self.geometry("300x200")

        # Create an instance of the LoginInterface and add it to the main window
        self.login_interface = LoginInterface(self)
        self.login_interface.pack()

    def switch_to_dashboard(self, dashboard_class):
        """
        This method switches the current display from the login interface to the specified dashboard.
        It first removes (forgets) the login interface and then packs the new dashboard interface into the window.

        :param dashboard_class: A class reference to the dashboard that should be displayed next.
        """
        # Remove the login interface from the window
        self.login_interface.pack_forget()

        # Create an instance of the specified dashboard class and display it
        self.dashboard = dashboard_class(self)
        self.dashboard.pack()

# This is the standard boilerplate for running a Python application.
# If this script is run (as opposed to being imported), create an instance of MainApplication and start the event loop.
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

