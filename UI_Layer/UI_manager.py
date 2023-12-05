from UI_header import UIHeader
from UI_login import LoginScreen
import UI_dashboard as db
import UI_manage_list as ml
import UI_modify_entries as me


class UIManager:
    def __init__(self, root):
        self.root = root
        self.current_screen = None
        self.page_history = []
        self.current_page_position = -1
        self.header = None
        self.possible_screens = {
            'LoginScreen': LoginScreen, 'PlanList': ml.PlanList, 'RefugeeList': ml.RefugeeList,
            'VolunteerList': ml.VolunteerList,
            'AdminDashboard': db.AdminDashboard, 'VolunteerDashboard': db.VolunteerDashboard, 'NewPlan': me.NewPlan,
            'EditPlan': me.EditPlan,
            'NewCamp': me.NewCamp, 'EditCamp': me.EditCamp, 'NewVolunteer': me.NewVolunteer,
            'EditVolunteer': me.EditVolunteer
        }
        self.logged_in_user = None

    def show_screen(self, screen_name: str, screen_data=None, add_to_history=True, *args):
        print(f"Showing screen: {screen_name}")
        self.clear_screen()

        if add_to_history:
            # The following if statement checks to see if the current page is the last item in the history.
            # If not the page history is reduced to include pages only up to the current page
            if self.current_page_position != len(self.page_history) - 1:
                self.page_history = self.page_history[:self.current_page_position]

            self.page_history.append((screen_name, screen_data))

            self.current_page_position += 1

        screen_class = self.possible_screens.get(screen_name)
        if not screen_class:
            print(f"Screen not found: {screen_name}")
            return

        if screen_class is LoginScreen and self.header:
            self.header.destroy()
            self.header = None
        elif self.header is None and screen_class is not LoginScreen:
            self.header = UIHeader(self.root, self.show_screen, screen_data, self.set_user, self.page_nav, self.reset_history, self.logged_in_user)
            self.header.pack(side='top', fill='x')

        self.current_screen = screen_class(self.root, self.show_screen, screen_data, self.set_user, self.page_nav, *args)
        self.current_screen.pack(expand=True, fill='both')
        print(self.page_history)

    def clear_screen(self):
        if self.current_screen is not None:
            print(f"Clearing screen: {type(self.current_screen)}")
            self.current_screen.destroy()
            self.current_screen = None
        else:
            print("No current screen to clear.")

    def page_nav(self, direction):
        if direction == 'back' and self.current_page_position > 0:
            if self.page_history[self.current_page_position - 1][0] == 'LoginScreen':
                print('Cannot navigate back to LoginScreen.')
                return
            self.current_page_position -= 1

        elif direction == 'forward' and self.current_page_position < len(self.page_history) - 1:
            self.current_page_position += 1

        elif direction == 'refresh':
            # this allows 'refresh' to be a valid input but simply executes showscreen without any navigation
            # changes or page history changes
            pass

        else:
            print('Invalid navigation direction or boundary reached.')
            return

        screen_name, screen_data = self.page_history[self.current_page_position]
        self.show_screen(screen_name, screen_data=screen_data, add_to_history=False)

    def reset_history(self):
        self.page_history = []
        self.current_page_position = -1
        self.logged_in_user = None

    def set_user(self, user):
        self.logged_in_user = user

