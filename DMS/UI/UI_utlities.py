import tkinter as tk
from tkinter import ttk

def create_filterable_treeview(parent, data_retrieval_methods, columns, on_double_click):
    search_frame = tk.Frame(parent, bg='white')
    search_frame.pack(pady=5, fill='x')
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side='left', padx=5, expand=True, fill='x')

    treeview = ttk.Treeview(parent, columns=columns)
    treeview.pack(expand=True, fill='both')
    for column in columns:
        treeview.heading(column, text=column)
        treeview.column(column, width=150)

    treeview.bind('<Double-1>', lambda event, tv=treeview: on_double_click(event, tv))

    def update_list():
        filter_value = search_entry.get().strip()
        if filter_value:
            filter_name, filter_value = filter_value.split(' ', 1)
            data = data_retrieval_methods['filtered'](filter_name, filter_value)
        else:
            data = data_retrieval_methods['all']()

        treeview.delete(*treeview.get_children())
        for item in data:
            treeview.insert("", "end", text=item['ID'], values=[item[column] for column in columns])

    filter_button = ttk.Button(search_frame, text="Filter/Search", command=update_list)
    filter_button.pack(side='left', padx=5)

    update_list()

    return treeview
