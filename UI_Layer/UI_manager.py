from UI_header import UIHeader
from UI_login import LoginScreen


class UIManager:
    def __init__(self, root):
        self.root = root
        self.current_screen = None
        self.page_history = []
        self.current_page_position = 0
        self.header = None

    def show_screen(self, screen_class, nav='not nav', *args):
        self.clear_screen()

        if screen_class is LoginScreen: # this makes sure the header is destroyed if the logout function is called
            self.page_history = [LoginScreen]
            self.current_page_position = 0
            if self.header is not None:
                self.header.destroy()
                self.header = None
        else:
            if self.header is None: # this makes sure no duplicate header frams are made when calling show_screen
                self.header = UIHeader(self.root, self.show_screen, self.page_nav, self.reset_history)
                self.header.pack(side='top', fill='x')
            else:
                # we can update the header with new information here
                pass

        # here i have integrated the header to exist at the top of any loaded frames
        # UIHeader.create_header(self.root).pack(side='top', fill='x')
        self.current_screen = screen_class(self.root, self.show_screen, *args)
        self.current_screen.pack(expand=True, fill='both')

        if nav == 'not nav':
            if self.current_page_position != len(self.page_history) - 1:
                self.page_history = self.page_history[:self.current_page_position + 1]

            self.page_history.append(screen_class)
        self.current_page_position = len(self.page_history) - 1
        print(self.page_history)

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()

    def page_nav(self, direction):
        if self.page_history == []:
            print('Navigation history is empty.')
            return

        next_position = None
        if direction == 'back':
            if self.current_page_position > 0:
                next_position = self.current_page_position - 1
            else:
                print('Already at the first page. Cannot navigate back.')
                return

        elif direction == 'forward':
            if self.current_page_position < len(self.page_history) - 1:
                next_position = self.current_page_position + 1
            else:
                print('Already at the last page. Cannot navigate forward.')
                return

        else:
            print('Invalid navigation direction.')
            return

        # Try to navigate to the new position
        try:
            self.show_screen(self.page_history[next_position], 'nav')
            self.current_page_position = next_position
        except Exception as e:
            print(f'Error during navigation: {e}')

    def reset_history(self):
        self.page_history.clear()
        self.current_page_position = 0

