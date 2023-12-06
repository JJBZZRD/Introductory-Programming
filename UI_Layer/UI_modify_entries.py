import tkinter as tk
from tkinter import ttk


# the name of this class might not explain the functionality very well as its quite an abstraction. This class
# produces varients of the pages to modfiy camps, plans, refugees, volunteers (and admins as personal details) There
# will be two varients for each subclass. adding new records and modfiying existing records
class ModifyEntries(tk.Frame):
    def __init__(self, ui_manager, **kwargs):
        super().__init__(ui_manager.root, **kwargs)
        self.root = ui_manager.root
        self.screen_data = ui_manager.screen_data
        self.show_screen = ui_manager.show_screen
        self.lower_frame = None
        self.modify_type = None  # this passes the title name information from the subclass to the 'def create_title(self):' method
        self.modifiable_variables: list = []  # this allows the subclass to pass the list of entry names to the ' def create_entry_fields(self):' method
        self.current_data = []  # this information is passed to be displayed in the entry fields only if it is an edit entry variant subclass being called
        self.entry_fields = {}  # this variable creates a dictionary that allows you to extract the values from the entry fields in 'def create_entry_fields(self):'
        self.button_labels = None
        self.setup_modify()

    def setup_modify(self):
        raise NotImplementedError("Subclasses should implement this method to setup the different entry modify pages")

    def create_title(self):
        # this method creates the title
        # page_top_frame = tk.Frame(self.root)
        # page_top_frame.pack(side='top')

        modify_title = ttk.Label(self, text=self.modify_type[0], font=("Helvetica", 20, "bold"))
        modify_title.pack(side='top', padx=10, pady=5)

    def create_entry_fields(self):
        # lower_frame = tk.Frame(self)
        self.lower_frame.pack(pady=10)
        entry_fields = {}
        # The ui logic to display the current values from the database within the entry boxes (read-only or
        # otherwise) is held in the following for loop

        k = 1
        j = 0
        for i, variable in enumerate(self.modifiable_variables):  # this loop creates a vertical list of columns that is 4 high maximum
            entry_name = ttk.Label(self.lower_frame, text=variable)
            entry_name.grid(column=k, row=j, pady=5, padx=5)

            entry_field = ttk.Entry(self.lower_frame)
            entry_field.grid(column=k + 1, row=j, pady=5, padx=5)



            self.entry_fields.update({variable: entry_field})

            if self.current_data is not None and i < len(self.current_data):
                placeholder = self.current_data[i]
            else:
                placeholder = "Enter " + variable

            entry_field.insert(0, placeholder)
            entry_field.bind("<FocusIn>", lambda event, e=entry_field, p=placeholder: self.on_focus_in(event, e, p))
            entry_field.bind("<FocusOut>", lambda event, e=entry_field, p=placeholder: self.on_focus_out(event, e, p))



            if j == 3:
                k += 2
                j = -1

            j += 1

    def on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def on_focus_out(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)

    def create_buttons(self):
        save_record = ttk.Button(self.lower_frame, text=self.button_labels, command=self.on_click_save_record)
        save_record.grid(column=5, row=4, padx=5, pady=5)

        spacer_button = ttk.Button(self.lower_frame, text=self.button_labels)
        spacer_button.grid()

        spacer_width = spacer_button.winfo_reqwidth() + 10

        spacer_button.grid_forget()

        spacer_frame = ttk.Frame(self.lower_frame, height=0, width=spacer_width)
        spacer_frame.grid(column=0, row=4)

    def on_click_save_record(self):
        # takes the entry field values
        inputs = []
        for key in self.entry_fields:
            inputs.append(self.entry_fields[key].get())
        
        # try to update data using the business logic function

        print(tuple(inputs))

        # if returns true 
            # return success message utility

        # if returns list
            # return error message utility with error list as input?



class NewPlan(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Plan']
        self.modifiable_variables = ['Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date']
        self.button_labels = 'Create'
        self.current_data = None
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
        self.modifiable_variables = ['Location', 'Shelter', 'Water Level', 'Food Level',
                                     'Medical supply']
        self.current_data = [self.screen_data.location, self.screen_data.shelter, self.screen_data.water,
                                     self.screen_data.food, self.screen_data.medical_supplies]
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
        self.current_data = ['JJ', 'Buzzard', '24/03/1997', '07780364693', 'camp1']
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()
        #print(self.entry_fields)


class NewRefugee(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['New Refugee']
        self.modifiable_variables = ['First Name', 'Last Name', 'Date of Birth', 'Phone Number', 'Camp']
        self.button_labels = 'Create'
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditRefugee(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Refugee']
        self.modifiable_variables = ['First Name', 'Last Name', 'Date of Birth', 'Family ID', 'Camp ID', 'Medical Condition']
        self.button_labels = 'Save Changes'
        self.current_data = [self.screen_data.first_name, self.screen_data.last_name, self.screen_data.date_of_birth, self.screen_data.familyID, self.screen_data.campID, self.screen_data.medical_condition]
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()


class EditPersonalDetails(ModifyEntries):
    def setup_modify(self):
        self.lower_frame = tk.Frame(self)
        self.modify_type = ['Edit Personal Details']
        self.modifiable_variables = ['First Name', 'Last Name', 'User Name', 'Date of Birth', 'Phone Number']
        self.button_labels = 'Save Changes'
        self.current_data = [self.screen_data.first_name, self.screen_data.last_name, self.screen_data.username, self.screen_data.date_of_birth, self.screen_data.phone]
        self.entry_fields = {}
        self.create_title()
        self.create_entry_fields()
        self.create_buttons()