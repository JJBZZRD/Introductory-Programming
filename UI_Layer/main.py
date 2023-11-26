import tkinter as tk
from UI_manager import UIManager
from UI_login import LoginScreen



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Refugee Management System")

    ui_manager = UIManager(root)

    # Initialize the first screen (LoginScreen)
    login_screen = LoginScreen(root, ui_manager.show_screen, ui_manager.reset_history)
    login_screen.pack(expand=True, fill='both')

    # Start the main event loop
    root.mainloop()
