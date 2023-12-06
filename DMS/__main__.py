import tkinter as tk
from .UI.UI_manager import UIManager


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Refugee Management System")

    ui_manager = UIManager(root)

    ui_manager.show_screen('LoginScreen')

    root.mainloop()
