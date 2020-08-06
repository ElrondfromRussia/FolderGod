import tkinter as tk


def make_labled_entry(tkwindow, name):
    row = tk.Frame(tkwindow)
    lab = tk.Label(row, width=10, text=name)
    ent = tk.Entry(row)
    ent.config(textvariable="")
    row.pack(side=tk.TOP, fill=tk.X)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, padx=2, pady=2)
    return ent
