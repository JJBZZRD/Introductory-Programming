from UI_header import UIHeader


class UIManager:
    def __init__(self, root):
        self.root = root
        self.current_screen = None
        self.page_history = []

    def show_screen(self, screen_class, *args):
        self.clear_screen()

        # here i have integrated the header to exist at the top of any loaded frames
        UIHeader.create_header(self.root).pack(side='top', fill='x')

        self.current_screen = screen_class(self.root, self.show_screen, *args)
        self.current_screen.pack(expand=True, fill='both')
        self.page_history.append(screen_class)

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()


