import dispatcher
import requests
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import os
import sys


path_to_watch = ""
THREAD = None


def set_path(p):
    global path_to_watch
    path_to_watch = p


def dispatch(t):
    global path_to_watch
    global EDITOR
    try:
        dispatcher.start_dispatching(path_to_watch, t)
    except BaseException as ex:
        print("EXCEPTION OCCURED: " + str(ex) + "\n")
        dispatch(t)


def money_loop():
    try:
        t = threading.currentThread()
        dispatch(t)
    except:
        pass


def make_dispatcher_close():
    try:
        with open(path_to_watch + "/ttttttttttttttt.tmp", 'tw', encoding='utf-8') as f:
            pass
        os.remove(path_to_watch + "/ttttttttttttttt.tmp")
    except BaseException as ex:
        sys.stderr.write("Can not close dispatcher: " + str(ex) + "\n")


###############################################
###############################################
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
###############################################
###############################################


try:
    window = tk.Tk()
    window.title("FolderGod")
    window.geometry('400x250')


    def on_start():
        global THREAD
        global path_to_watch
        if not THREAD:
            print("Start dispatching...")
            path_to_watch = editor.get()
            info_thread = threading.Thread(target=money_loop, args=())
            info_thread.start()
            info_thread.do_disp = True
            THREAD = info_thread
            btn.config(text="stop", background="#ff0000")
        else:
            print("Stop dispatching...")
            THREAD.do_disp = False
            THREAD = None
            make_dispatcher_close()
            btn.config(text="start", background="#00ff00")


    editor = tk.Entry(window, font=("Consolas", 10), text=path_to_watch, width=50)
    editor.pack(side=tk.TOP)
    editor.insert(0, path_to_watch)
    EDITOR = editor

    btn = tk.Button(window, text="start", background="#00ff00", command=on_start, pady=2, bd=4, relief=tk.GROOVE)
    btn.pack()

    shower = tk.scrolledtext.ScrolledText(window, width=100, height=60, font=("Consolas", 10))
    shower.pack(side=tk.BOTTOM)
    shower.tag_configure("stderr", foreground="#ff0000")
    shower.tag_configure("stdout", foreground="#0000ff")
    sys.stdout = TextRedirector(shower, "stdout")
    sys.stderr = TextRedirector(shower, "stderr")

    ###############################################
    def on_closing():
        global THREAD
        if THREAD:
            THREAD.do_disp = False
            make_dispatcher_close()
        window.destroy()

    ###############################################
    def on_mouse_down(event):
        global dif_x, dif_y
        win_position = [int(coord) for coord in window.wm_geometry().split('+')[1:]]
        dif_x, dif_y = win_position[0] - event.x_root, win_position[1] - event.y_root

    ###############################################
    def update_position(event):
        window.wm_geometry("+%d+%d" % (event.x_root + dif_x, event.y_root + dif_y))


    #window.bind('<ButtonPress-1>', on_mouse_down)
    #window.bind('<B1-Motion>', update_position)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
except BaseException as ex:
    sys.stderr.write("Ohoohooooo..." + str(ex) + "\n")
