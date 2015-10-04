# coding: utf-8
"""handle the main window of the View"""
from tkinter import Frame


class MainWindow(Frame):

    def __init__(self, master=None, datacontext=None):
        """init the Frame instance"""
        Frame.__init__(self, master)
        self._datacontext = datacontext
        self.init()

    def init(self):
        self.master.title("mtx-View")
        self.grid(stick='EWSN')
        self.grid_propagate(1)
        self.columnconfigure(0, weight=1)

    @property
    def datacontext(self):
        return self._datacontext

    @datacontext.setter
    def datacontext(self, value):
        self._datacontext = value
