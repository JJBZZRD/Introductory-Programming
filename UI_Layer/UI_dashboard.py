import tkinter as tk
from tkinter import ttk
from UI_header import UIHeader
from UI_dashboard import AdminDashboard

class AdminPlansScreen(tk.Frame):
    def __init__(self, root, callback, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        # Create the header
        self.header = UIHeader.create_header(self)
        self.header.pack(side=tk.TOP, fill=tk.X)

        # Main content Frame
        content_frame = tk.Frame(self)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Search field
        tk.Label(content_frame, text="Search by name").grid(row=0, column=0, sticky='w')
        search_entry = tk.Entry(content_frame)
        search_entry.grid(row=0, column=1, sticky='we')
        search_button = tk.Button(content_frame, text="Search")
        search_button.grid(row=0, column=2, padx=10)

        # Add new plan button
        add_plan_button = tk.Button(content_frame, text="Add new plan")
        add_plan_button.grid(row=0, column=3)

        # Table for the plans
        columns = ('Plan Name', 'Plan Type', 'Region', 'Description', 'Start Date', 'End Date')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.grid(row=1, column=0, columnspan=4, sticky='nsew')

        # Bind the double-click event to the on_item_double_click function
        tree.bind("<Double-1>", self.on_item_double_click)

        # Dummy data for the treeview
        plans = [
            ("Plan 1", "Type A", "Region 1", "Description 1", "1/1/2023", "1/1/2024"),
            # Add more dummy data as needed
        ]
        for plan in plans:
            tree.insert('', 'end', values=plan)

        # Configuring row and column weights
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

    def on_item_double_click(self, event):
        # Use callback to transition to the admin dashboard
        self.callback(AdminDashboard)