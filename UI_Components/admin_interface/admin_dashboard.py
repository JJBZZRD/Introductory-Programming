# admin_dashboard.py

import tkinter as tk
from tkinter import ttk
from header_ui import create_header

# Placeholder functions for future logic
def manage_volunteers():
    pass  # Placeholder for future manage volunteers logic

def search_volunteers():
    pass  # Placeholder for future search volunteers logic

def view_volunteer_details():
    pass  # Placeholder for future view volunteer details logic

def allocate_resources():
    pass  # Placeholder for future resource allocation logic

def show_admin_dashboard(root):
    # Destroy the login window
    root.destroy()
    
    admin_root = tk.Tk()
    admin_root.title("Admin Dashboard")

    # Create and pack the header at the top of the dashboard window
    header = create_header(admin_root)
    header.pack(side=tk.TOP, fill=tk.X)

    # Create a container for volunteer and resources frames
    container = tk.Frame(admin_root)
    container.pack(fill=tk.BOTH, expand=True)

    # Volunteer frame (on the left side)
    volunteer_frame = tk.Frame(container, padx=10, pady=10)
    volunteer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Placeholder for volunteer management
    manage_volunteers_button = tk.Button(volunteer_frame, text="Manage Volunteers", command=manage_volunteers)
    manage_volunteers_button.pack(pady=10)

    # Search and filter area for volunteers
    search_entry = tk.Entry(volunteer_frame, width=50)
    search_entry.pack(side=tk.TOP, fill=tk.X)
    search_button = tk.Button(volunteer_frame, text="Search", command=search_volunteers)
    search_button.pack(side=tk.TOP, pady=5)

    # Placeholder for volunteer list
    for i in range(3):
        individual_volunteer_frame = tk.Frame(volunteer_frame, pady=5)
        individual_volunteer_frame.pack(fill=tk.X)

        pic_label = tk.Label(individual_volunteer_frame, text="PIC", bg="blue", width=5)
        pic_label.pack(side=tk.LEFT)

        name_label = tk.Label(individual_volunteer_frame, text=f"Volunteer {i+1}")
        name_label.pack(side=tk.LEFT, padx=10)

        details_button = tk.Button(individual_volunteer_frame, text="Details", command=view_volunteer_details)
        details_button.pack(side=tk.RIGHT)

     # Resource allocation frame (on the right side)
    resource_allocation_frame = tk.Frame(container, padx=10, pady=10)
    resource_allocation_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Summary of resource allocation
    resource_summary_label = tk.Label(resource_allocation_frame, text="Resource Allocation Summary", font=("Helvetica", 14))
    resource_summary_label.pack(pady=(0, 10))

    # Placeholder for resource summary information
    for resource in ["Tents allocated:", "Medical supplies:", "Food servings:"]:
        tk.Label(resource_allocation_frame, text=f"{resource} [Mock Data]").pack()

    # Button to allocate resources
    allocate_resources_button = tk.Button(resource_allocation_frame, text="Allocate Resources", command=allocate_resources)
    allocate_resources_button.pack(pady=10)

    # Start the main loop for the admin dashboard
    admin_root.mainloop()

# This would be placed in your main app file where the admin dashboard is triggered
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login")
    show_admin_dashboard(root)
    root.mainloop()
