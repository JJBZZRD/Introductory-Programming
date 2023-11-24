from UI_header import UIHeader


class UIManager:
    def __init__(self, root):
        self.root = root
        self.current_screen = None
        self.page_history = []
        self.header = None

    def show_screen(self, screen_class, *args):
        self.clear_screen()

        if not self.header:
            self.header = UIHeader.create_header(self.root)
            self.header.pack(side='top', fill='x')
        else:
            # we can update the header with new information here
            pass

        # here i have integrated the header to exist at the top of any loaded frames
        #UIHeader.create_header(self.root).pack(side='top', fill='x')
        self.current_screen = screen_class(self.root, self.show_screen, *args)
        self.current_screen.pack(expand=True, fill='both')
        self.page_history.append(screen_class)

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()


