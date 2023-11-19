import tkinter as tk
from tkinter import ttk
from header_ui import create_header


# Placeholder functions for future logic
def manage_resources():
    pass  # Placeholder for future manage resources logic

def search_refugees():
    pass  # Placeholder for future search refugees logic

def view_details():
    pass  # Placeholder for future view details logic

def logout(volunteer_root):
    volunteer_root.destroy()  # Destroy the dashboard window

def show_volunteer_dashboard(root):
    # Destroy the login window
    root.destroy()
    
    volunteer_root = tk.Tk()
    volunteer_root.title("Volunteer Dashboard")

    # Create and pack the header at the top of the dashboard window
    header = create_header(volunteer_root)
    header.pack(side=tk.TOP, fill=tk.X)

    # Create a container for resource and refugees frames
    container = tk.Frame(volunteer_root)
    container.pack(fill=tk.BOTH, expand=True)

    # Resource frame (on the left side)
    resource_frame = tk.Frame(container, padx=10, pady=10)
    resource_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Placeholder for resource indicators
    for resource in ["Housing", "Food", "Water"]:
        resource_label = tk.Label(resource_frame, text=resource)
        resource_label.pack()
        progress = ttk.Progressbar(resource_frame, length=200, value=70)
        progress.pack()

    manage_resources_button = tk.Button(resource_frame, text="Manage resources", command=manage_resources)
    manage_resources_button.pack(pady=10)

    # Refugees frame (on the right side)
    refugees_frame = tk.Frame(container, padx=10, pady=10)
    refugees_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Search and filter area
    search_entry = tk.Entry(refugees_frame, width=50)
    search_entry.pack(side=tk.TOP, fill=tk.X)
    search_button = tk.Button(refugees_frame, text="Search", command=search_refugees)
    search_button.pack(side=tk.TOP, pady=5)

    # Placeholder for refugee list
    for i in range(3):
        refugee_frame = tk.Frame(refugees_frame, pady=5)
        refugee_frame.pack(fill=tk.X)

        pic_label = tk.Label(refugee_frame, text="PIC", bg="green", width=5)
        pic_label.pack(side=tk.LEFT)

        name_label = tk.Label(refugee_frame, text=f"Name {i+1}")
        name_label.pack(side=tk.LEFT, padx=10)

        details_button = tk.Button(refugee_frame, text="Details", command=view_details)
        details_button.pack(side=tk.RIGHT)

    # Bottom frame for logout and navigation
    bottom_frame = tk.Frame(volunteer_root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    logout_button = tk.Button(bottom_frame, text="Logout", command=lambda: logout(volunteer_root))
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Start the main loop for the volunteer dashboard
    volunteer_root.mainloop()
