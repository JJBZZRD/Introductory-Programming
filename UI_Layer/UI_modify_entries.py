import tkinter as tk
from tkinter import ttk


# the name of this class might not explain the functionality very well as its quite an abstraction. This class
# produces varients of the pages to modfiy camps, plans, refugees, volunteers (and admins as personal details) There
# will be two varients for each subclass. adding new records and modfiying existing records
class ModifyEntries(tk.Frame):
    def __init__(self, root, show_screen, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.show_screen = show_screen
        self.setup_modify()
        self.lower_frame = None
        self.modify_type = None  # this passes the title name information from the subclass to the 'def create_title(self):' method
        self.modifiable_variables: list = None  # this allows the subclass to pass the list of entry names to the ' def create_entry_fields(self):' method
        self.entry_fields = None  # this variable creates a dictionary that allows you to extract the values from the entry fields in 'def create_entry_fields(self):'
        self.button_labels = None

    def setup_modify(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different entry modify pages")

    def create_title(self):
        # this method creates the title and add entry button for each list
        # page_top_frame = tk.Frame(self.root)
        # page_top_frame.pack(side='top')

        modify_title = ttk.Label(self, text=self.modify_type[0], font=("Helvetica", 20, "bold"))
        modify_title.pack(side='top', padx=10, pady=5)

    def create_entry_fields(self):
        # lower_frame = tk.Frame(self)
        self.lower_frame.pack(pady=10)

        # The ui logic to display the current values from the database within the entry boxes (read-only or
        # otherwise) is held in the following for loop

        k = 1
        j = 0
        for i in self.modifiable_variables:  # this loop creates a vertical list of columns that is 4 high maximum
            entry_name = ttk.Label(self.lower_frame, text=i)
            entry_name.grid(column=k, row=j, pady=5, padx=5)

            entry_field = ttk.Entry(self.lower_frame)
            entry_field.grid(column=k + 1, row=j, pady=5, padx=5)

            self.entry_fields[i] = entry_field

            if j == 3:
                k += 2
                j = -1

            j += 1

    def create_buttons(self):
        save_record = ttk.Button(self.lower_frame, text=self.button_labels)
        save_record.grid(column=5, row=4, padx=5, pady=5)

        spacer_button = ttk.Button(self.lower_frame, text=self.button_labels)
        spacer_button.grid()

        spacer_width = spacer_button.winfo_reqwidth() + 10

        spacer_button.grid_forget()

        spacer_frame = ttk.Frame(self.lower_frame, height=0, width=spacer_width)
        spacer_frame.grid(column=0, row=4)


class NewPlan(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Plan']
        self.modifiable_variables = ['Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date']
        self.button_labels = 'Create'
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditPlan(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Plan']
        self.modifiable_variables = ['Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date']
        self.button_labels = 'Save Changes'
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class NewCamp(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Camp']
        self.modifiable_variables = ['Camp Name', 'Refugees', 'Volunteers', 'Water Level', 'Food Level',
                                     'Medical supply']
        self.button_labels = 'Create'
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditCamp(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Camp']
        self.modifiable_variables = ['Camp Name', 'Refugees', 'Volunteers', 'Water Level', 'Food Level',
                                     'Medical supply']
        self.button_labels = 'Save Changes'
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class NewVolunteer(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Volunteer']
        self.modifiable_variables = ['First Name', 'Last Name', 'Date of Birth', 'Phone Number', 'Camp']
        self.button_labels = 'Create'
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditVolunteer(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Volunteer']
        self.modifiable_variables = ['First Name', 'Last Name', 'Date of Birth', 'Phone Number', 'Camp']
        self.button_labels = 'Save Changes'
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()
