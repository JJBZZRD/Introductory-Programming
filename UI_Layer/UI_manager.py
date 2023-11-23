import tkinter as tk
from UI_login import LoginScreen
from UI_dashboard import AdminDashboard, VolunteerDashboard

class UIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Refugee Management System")
        self.current_screen = None

    def run(self):
        self.show_screen(LoginScreen)
        self.root.mainloop()

    def show_screen(self, screen_class, *args):
        self.clear_screen()
        self.current_screen = screen_class(self.root, self.change_screen, *args)
        self.current_screen.pack(expand=True, fill='both')

    def change_screen(self, next_screen_class, *args):
        self.show_screen(next_screen_class, *args)

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()

if __name__ == "__main__":
    app = UIManager()
    app.run()
