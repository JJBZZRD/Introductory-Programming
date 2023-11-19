import tkinter as tk
from tkinter import ttk
from .header_ui import Header  # Make sure this import matches the structure of your project

class VolunteerDashboard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg='white')  # Assuming a white background
        self.create_widgets()

    def create_widgets(self):
        # Create and pack the header at the top of the dashboard
        self.header = Header(self, title="CAMP 1", mode_callback=self.handle_mode_change)
        self.header.pack(side='top', fill='x')

        # Resources frame
        resources_frame = tk.LabelFrame(self, text='Resources', padx=10, pady=10, bg='white')
        resources_frame.pack(side='left', fill='y', expand=False)

        # Sample data for resources
        resources = [('Shelter', 4, 10), ('Food', 7, 10), ('Water', 6, 10)]
        for resource, used, capacity in resources:
            tk.Label(resources_frame, text=resource, bg='white').pack()
            progress = ttk.Progressbar(resources_frame, length=200, maximum=capacity)
            progress.pack(padx=10, pady=2)
            progress['value'] = used
            tk.Label(resources_frame, text=f'{used}/{capacity} (usage/capacity)', bg='white').pack()

        tk.Button(resources_frame, text='Manage resources', bg='blue', fg='white').pack(pady=10)

        # Refugees frame
        refugees_frame = tk.LabelFrame(self, text='Refugees', padx=10, pady=10, bg='white')
        refugees_frame.pack(side='left', fill='both', expand=True)

        # Sample data for refugees
        refugees = ['Name1', 'Name2', 'Name3']
        for name in refugees:
            refugee_frame = tk.Frame(refugees_frame, bg='white')
            refugee_frame.pack(fill='x', padx=10, pady=2)
            tk.Label(refugee_frame, text='PIC', bg='white').pack(side='left')
            name_label = tk.Label(refugee_frame, text=name, bg='white')
            name_label.pack(side='left', padx=10)
            details_button = tk.Button(refugee_frame, text='Details', bg='blue', fg='white')
            details_button.pack(side='right')

        # Assuming a bottom section for additional management features
        manage_frame = tk.Frame(self, bg='lightgray', height=50)
        manage_frame.pack(side='bottom', fill='x')
        tk.Button(manage_frame, text='Manage resources', bg='blue', fg='white').pack(side='right', pady=10)

    # Placeholder functions for event handling
    def manage_resources(self):
        pass

    def show_refugee_details(self):
        pass

    def handle_mode_change(self, new_mode):
        # Handle the mode change here (e.g., update the UI or application state)
        print(f"Mode changed to: {new_mode}")

# To test this module independently, you can create a root Tk instance and pack this dashboard into it.
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = VolunteerDashboard(root)
    dashboard.pack(side="top", fill="both", expand=True)
    root.mainloop()
