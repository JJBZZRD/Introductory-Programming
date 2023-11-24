import tkinter as tk
from tkinter import ttk


# the name of this class might not explain the functionality very well as its quite an abstraction.
# This class produces varients of the pages to modfiy camps, plans, refugees, volunteers (and admins as personal details)
# There will be two varients for each subclass. adding new records and modfiying existing records
class ModifyEntries(tk.Frame):
    def __init__(self, root, show_screen, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.show_screen = show_screen
        self.setup_modify()
        self.modify_type = None

    def setup_modify(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different entry modify pages")

    def create_title(self):
        # this method creates the title and add entry button for each list
        # page_top_frame = tk.Frame(self.root)
        # page_top_frame.pack(side='top')

        modify_title = ttk.Label(self, text=self.modify_type[0], font=("Helvetica", 20, "bold"))
        modify_title.pack(side='top', padx=10, pady=5)


    def create_entry_fields(self):
        lower_frame = tk.Frame(self)
        lower_frame.pack(pady=10)


class ModifyPlan(ModifyEntries):
    def setup_modify(self):
        self.modify_type = ['New Plan']
        self.create_title()
