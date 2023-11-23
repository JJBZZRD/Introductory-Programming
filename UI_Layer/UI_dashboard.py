import tkinter as tk
from tkinter import ttk
from UI_header import UIHeader

class Dashboard(tk.Frame):
    def __init__(self, root, callback, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.header = UIHeader.create_header(self)
        self.header.pack(side=tk.TOP, fill=tk.X)
        self.setup_dashboard()

    def setup_dashboard(self):
        raise NotImplementedError("Subclasses should implement this method to setup the dashboard layout")
    
    def populate_overview_tab(self, tab):
        # Create a frame for the additional resources
        additional_resources_frame = tk.Frame(tab, bg='lightgray', bd=2, relief='groove')
        additional_resources_frame.pack(side='right', fill='y', padx=(5, 0))

        # Add a label for the additional resources section
        tk.Label(additional_resources_frame, text="Additional Resources Available", bg='lightgray').pack(pady=10)

        # This is a placeholder for actual data and widgets for additional resources
        tk.Label(additional_resources_frame, text="[Data]", bg='lightgray').pack()

        # Create a canvas for the bar charts in the overview
        canvas = tk.Canvas(tab, bg='white')
        canvas.pack(expand=True, fill='both', side='left')

        # Sample data for the bar chart
        resources = [('Tents', 80), ('Food', 60), ('Water', 50), ('Medicine', 30)]

        # Draw the bar chart
        for i, (resource, percent) in enumerate(resources):
            self.draw_bar(canvas, i, resource, percent)

    
    def populate_camp_tab(self, tab, camp_number):
        # Create the canvas for drawing resource bars
        canvas = tk.Canvas(tab, bg='white')
        canvas.pack(side='left', expand=True, fill='both')

        # Sample data for resources in a specific camp
        resources = {
            'Tents': {'total': 10, 'allocated': 4},
            'Food': {'total': 10, 'allocated': 7},
            'Water': {'total': 10, 'allocated': 6},
            'Medicine': {'total': 10, 'allocated': 6}
        }

        # Create a frame for the resource indicators
        resource_frame = tk.Frame(tab, bg='white')
        resource_frame.pack(side='left', fill='y')

        for resource, counts in resources.items():
            self.create_resource_indicator(resource_frame, resource, counts['allocated'], counts['total'])

    def create_resource_indicator(self, root, resource, allocated, total):
        # This creates each resource indicator bar along with +/- buttons
        frame = tk.Frame(root, bg='white')
        frame.pack(pady=5, fill='x', padx=10)

        # Resource icon (just a placeholder label here)
        icon_label = tk.Label(frame, text=f'Icon {resource}', bg='white')
        icon_label.pack(side='left')

        # Bar chart for the resource
        bar = ttk.Progressbar(frame, orient='horizontal', length=100, mode='determinate')
        bar['value'] = (allocated / total) * 100
        bar.pack(side='left', padx=(5, 0))

        # Add buttons for adjusting resource allocation
        add_button = tk.Button(frame, text='+', command=lambda: self.adjust_resource(resource, 1))
        sub_button = tk.Button(frame, text='-', command=lambda: self.adjust_resource(resource, -1))
        add_button.pack(side='left', padx=2)
        sub_button.pack(side='left', padx=2)

    def draw_bar(self, canvas, index, resource, percent):
        # Draw a single bar in the canvas for a given resource
        x0 = 50 + index * 100  # x-coordinate for the bar
        y0 = 150              # y-coordinate for the bottom of the bar
        x1 = x0 + 20          # width of the bar
        y1 = y0 - percent     # height of the bar (based on percentage)
        canvas.create_rectangle(x0, y0, x1, y1, fill='gray', outline='black')
        # Label for the resource
        canvas.create_text(x0 + 10, y0 + 10, text=f'{resource}', anchor='n')

    
    def adjust_resource(self, resource, adjustment):
        # Placeholder method to adjust resources
        pass

class AdminDashboard(Dashboard):
    def setup_dashboard(self):
        self.create_camp_tabs()

    def create_camp_tabs(self):
        self.tab_control = ttk.Notebook(self)
        
        # Create an overview tab
        self.overview_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text='Overview')
        self.populate_overview_tab(self.overview_tab)
        
        # Add tabs dynamically based on the number of camps
        for i in range(1, 4):
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=f'Camp {i}')
            self.populate_camp_tab(tab, i)
        
        self.tab_control.pack(expand=1, fill="both")
    

class VolunteerDashboard(Dashboard):
    def setup_dashboard(self):
        self.create_volunteer_camp_tab()

    def create_volunteer_camp_tab(self):
        # Initialize a Notebook widget
        self.tab_control = ttk.Notebook(self)

        # Create a single tab for Camp 1
        self.camp_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.camp_tab, text='Camp 1')
        
        # Populate the camp tab with relevant widgets and data
        self.populate_camp_tab(self.camp_tab, 1)

        # Pack the Notebook widget
        self.tab_control.pack(expand=1, fill="both")
