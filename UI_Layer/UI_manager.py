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

        if screen_class is LoginScreen:
            if self.header is not None:
                self.header.destroy()
                self.header = None
        else:
            if self.header is None:
                self.header = UIHeader(self.root, self.show_screen, self.page_nav)
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

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()

    def page_nav(self, direction):
        try:
            if direction == 'back':
                if self.current_page_position == 0:
                    pass
                self.show_screen(self.page_history[self.current_page_position - 1], 'nav')

            elif direction == 'forward':
                self.show_screen(self.page_history[self.current_page_position + 1], 'nav')
        except:
            print('invalid direction')
