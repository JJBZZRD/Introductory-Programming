from .UI_header import UIHeader
from .UI_login import LoginScreen
from . import UI_dashboard as db
from . import UI_manage_list as ml
from . import UI_modify_entries as me


class UIManager:
    """
    Handles page rendering, navigation history, and user session management.

    Attributes:
        root (tkinter.Tk): The root window of the tkinter application.
        current_screen (tkinter.Frame): The currently displayed screen/frame in the application.
        page_history (list): A list to track the navigation history of screens.
        current_page_position (int): The current position in the navigation history.
        header (UIHeader): The header component of the UI, if applicable.
        possible_screens (dict): A dictionary mapping screen names to their respective classes.
        logged_in_user: The user object representing the currently logged-in user, if any.
    """

    def __init__(self, root):
        self.root = root
        self.current_screen = None
        self.page_history = []
        self.current_page_position = -1
        self.header = None
        self.possible_screens = {
            "LoginScreen": LoginScreen,
            "PlanList": ml.PlanList,
            "RefugeeList": ml.RefugeeList,
            "VolunteerList": ml.VolunteerList,
            "AdminDashboard": db.AdminDashboard,
            "VolunteerDashboard": db.VolunteerDashboard,
            "NewPlan": me.NewPlan,
            "EditPlan": me.EditPlan,
            "NewCamp": me.NewCamp,
            "EditCamp": me.EditCamp,
            "NewVolunteer": me.NewVolunteer,
            "EditVolunteer": me.EditVolunteer,
            "EditPersonalDetails": me.EditPersonalDetails,
            "NewRefugee": me.NewRefugee,
            "EditRefugee": me.EditRefugee,
            "CampList": ml.CampList,
            "AuditLogs": ml.AuditLogs,
        }
        self.logged_in_user = None
        self.screen_data = None

    def show_screen(
        self,
        screen_name: str,
        screen_data: any = None,
        add_to_history: bool = True,
        *args,
    ):
        """
        Displays the specified screen in the UI. Manages the header and updates navigation history.

        Args:
            screen_name (str): Next screen to be displayed.
            screen_data (optional): Data to be passed to the next screen. Defaults to None.
            add_to_history (bool, optional): If True, adds the screen to the navigation history. Defaults to True.
            *args: Additional arguments to be passed to the screen constructor.
        """

        self.clear_screen()

        screen_class = self.possible_screens.get(screen_name)

        if screen_data is not None:
            self.screen_data = screen_data
        else:
            self.screen_data = None

        if add_to_history:
            # The following if statement checks to see if the current page is the last item in the history.
            # If not the page history is reduced to include pages only up to the current page
            if self.current_page_position != len(self.page_history) - 1:
                self.page_history = self.page_history[: self.current_page_position + 1]

            # The following if statement makes sure that pressing the same button multiple times doesn't add
            # to the page history or position
            if screen_class is LoginScreen or (
                len(self.page_history) > 0 and screen_name != self.page_history[-1][0]
            ):
                self.page_history.append((screen_name, screen_data))
                self.current_page_position += 1

        if not screen_class:
            print(f"Screen not found: {screen_name}")
            return

        if screen_class is LoginScreen and self.header:
            self.header.destroy()
            self.header = None
        elif self.header is None and screen_class is not LoginScreen:
            self.header = UIHeader(self, *args)
            self.header.pack(side="top", fill="x")

        self.current_screen = screen_class(self, *args)
        self.current_screen.pack(expand=True, fill="both")

        list = []
        for i in self.page_history:
            list.append(i[0])

        # print(list)

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None
        else:
            print("No current screen to clear.")

    def page_nav(self, direction):
        if direction == "back" and self.current_page_position > 0:
            if self.page_history[self.current_page_position - 1][0] == "LoginScreen":
                print("Cannot navigate back to LoginScreen.")
                return
            self.current_page_position -= 1

        elif (
            direction == "forward"
            and self.current_page_position < len(self.page_history) - 1
        ):
            self.current_page_position += 1
        else:
            print("Invalid navigation direction or boundary reached.")
            return

        screen_name, screen_data = self.page_history[self.current_page_position]
        self.show_screen(screen_name, screen_data=screen_data, add_to_history=False)

    def refresh_page(self):
        if self.page_history[self.current_page_position - 1][0] == "LoginScreen":
            self.page_nav("forward")
            self.page_nav("back")
        else:
            self.page_nav("back")
            self.page_nav("forward")

    def reset_history(self):
        self.page_history = []
        self.current_page_position = -1
        self.logged_in_user = None

    def set_user(self, user):
        self.logged_in_user = user
