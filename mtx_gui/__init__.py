# coding: utf-8
from tkinter import Tk, messagebox


from mtx_gui.View.MainWindow import *
from mtx_gui.Model.api import *

if __name__ == "__main__":
    try:
        _medium_changers = get_medium_changers()
        root = Tk()
        root.config(height=400)
        root.grid_propagate(1)
        root.resizable(0,0)
        guiFrame = MainWindow(root, medium_changers=_medium_changers)
        root.mainloop()
    except Exception as e:
        messagebox.showinfo(title='mtxgui info', message=str(e))
