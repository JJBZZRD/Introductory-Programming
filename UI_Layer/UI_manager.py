import tkinter as tk
from UI_login import LoginScreen

class UIManager:
    def __init__(self, root):
        self.root = root
        self.current_screen = None

    def show_screen(self, screen_class, *args):
        self.clear_screen()
        self.current_screen = screen_class(self.root, self.show_screen, *args)
        self.current_screen.pack(expand=True, fill='both')

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()

def run_application():
    root = tk.Tk()
    root.title("Refugee Management System")

    ui_manager = UIManager(root)  # Create an instance of UIManager

    login_screen = LoginScreen(root, ui_manager.show_screen)  # Pass show_screen method to LoginScreen
    login_screen.pack(expand=True, fill='both')

    root.mainloop()

if __name__ == "__main__":
    run_application()
