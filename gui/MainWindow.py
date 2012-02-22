# coding: utf-8
'''handle the main window of the Gui'''

import os
from Tkinter import *
import tkMessageBox

from widgets import *

class MainWindow(Frame):

    def __init__(self, master=None,medium_changers=None):
        ''' init the Frame instance'''
        Frame.__init__(self,master)
        self._storageframe = None
        self._dataframe = None
        self._changerframe = None
        self._mediumchangers = medium_changers
        self.master.title("mtx-gui")
        self.grid(stick='EWSN')
        self.grid_propagate(1)
        self.columnconfigure(0,weight= 1)
        self.createWidgets()


    @property
    def mediumchangers(self):
        return self._mediumchangers
    @property
    def storageframe(self):
        return self._storageframe

    @storageframe.setter
    def storageframe(self, value):
        self._storageframe = value

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        self._dataframe = value

    @property
    def changerframe(self):
        return self._changerframe

    @changerframe.setter
    def changerframe(self, value):
        self._changerframe = value

    def createWidgets(self):
        self.changerframe = ChangerFrame(self,self.mediumchangers)
        self.statusbar = StatusBar(self)