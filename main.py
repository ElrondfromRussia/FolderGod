import dispatcher
import utils
import smtp_sender
import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import sys

path_to_watch = ""
THREAD = None
EDITOR = None
SRV = None
USR = None
PSW = None
TO = None
# TODO: use INTERVAL for dispatcher
INTERVAL = None


###############################################
###############################################
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.yview("end")
        self.widget.configure(state="disabled")

    def flush(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


###############################################
###############################################


def set_path(p):
    global path_to_watch
    path_to_watch = p


def dispatch(t):
    global path_to_watch
    global EDITOR, THREAD
    try:
        dispatcher.start_dispatching(path_to_watch, t)
    except BaseException as e:
        print("EXCEPTION OCCURED: " + str(e) + "\n")
        # dispatch(t)
        raise e


def money_loop():
    global THREAD
    try:
        t = threading.currentThread()
        dispatch(t)
    except BaseException as e:
        raise e


def make_dispatcher_close():
    try:
        with open(path_to_watch + "/ttttttttttttttt.tmp", 'tw', encoding='utf-8') as f:
            pass
        os.remove(path_to_watch + "/ttttttttttttttt.tmp")
    except BaseException as ex:
        sys.stderr.write("Can not close dispatcher: " + str(ex) + "\n")
        raise ex


try:
    window = tk.Tk()
    window.title("FolderGod")
    window.geometry('600x400')


    ###############################################
    def on_start():
        try:
            global THREAD
            global EDITOR
            global path_to_watch
            if not THREAD:
                print("Start dispatching...", EDITOR.get())
                smtp_sender.set_smtp_settings(USR.get(), PSW.get(), SRV.get(), TO.get())
                dispatcher.set_mailing_interval(INTERVAL.get())
                path_to_watch = EDITOR.get()
                info_thread = threading.Thread(target=money_loop, args=())
                info_thread.start()
                info_thread.do_disp = True
                THREAD = info_thread
                btn.config(text="STOP", background="#ff0000")
            else:
                print("Stop dispatching...")
                THREAD.do_disp = False
                THREAD = None
                make_dispatcher_close()
                btn.config(text="START", background="#00ff00")
        except BaseException as e:
            print("Stop dispatching with error...", e)
            THREAD = None
            btn.config(text="START", background="#00ff00")


    ###############################################

    SRV = utils.make_labled_entry(window, 'Servername', 'Servername')
    USR = utils.make_labled_entry(window, 'User', 'User')
    PSW = utils.make_labled_entry(window, 'Password', 'Password')
    TO = utils.make_labled_entry(window, 'Send to', 'Send to (supports list: a@bb.ru; b@bb.ru)')
    INTERVAL = utils.make_labled_entry(window, 'Interval', 'Interval of mailing (min)')
    EDITOR = utils.make_labled_entry(window, 'Path to watch', 'Path to watch')

    btn = tk.Button(window, text="START", background="#00ff00", command=on_start, pady=2, bd=4, relief=tk.GROOVE)
    btn.pack(expand=tk.YES, fill=tk.X, padx=2, pady=2)

    shower = tk.scrolledtext.ScrolledText(window, font=("Consolas", 10))
    shower.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH, padx=2, pady=2)
    shower.tag_configure("stderr", foreground="#ff0000")
    shower.tag_configure("stdout", foreground="#0000ff")
    sys.stdout = TextRedirector(shower, "stdout")
    sys.stderr = TextRedirector(shower, "stderr")


    ###############################################
    def on_closing():
        global THREAD
        try:
            if THREAD:
                on_start()
        finally:
            window.destroy()


    ###############################################
    def on_mouse_down(event):
        global dif_x, dif_y
        win_position = [int(coord) for coord in window.wm_geometry().split('+')[1:]]
        dif_x, dif_y = win_position[0] - event.x_root, win_position[1] - event.y_root


    ###############################################
    def update_position(event):
        window.wm_geometry("+%d+%d" % (event.x_root + dif_x, event.y_root + dif_y))


    ###############################################

    # moving when clicked any place
    # window.bind('<ButtonPress-1>', on_mouse_down)
    # window.bind('<B1-Motion>', update_position)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
except BaseException as ex:
    sys.stderr.write("Ohoohooooo..." + str(ex) + "\n")
