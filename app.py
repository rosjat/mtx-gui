# coding: utf-8

from gui.MainWindow import *
from api import *

if __name__ == "__main__":
    try:
        _medium_changers = get_medium_changers()
        root = Tk()
        root.config(width = 900, height = 400)
        root.grid_propagate(0)
        root.resizable(0,0)
        guiFrame = MainWindow(root,medium_changers = _medium_changers)
        root.mainloop()
    except Exception as e:
        tkMessageBox.showinfo(title='mtxgui info', \
                                 message= str(e))