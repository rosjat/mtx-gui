# coding: utf-8
"""collection of the widgets that are used in the View"""
from tkinter import Button, PhotoImage
from .frame import DataFrame, StorageFrame
from . import _imagepath


class MediumChangerButton(Button):

    def __init__(self, parent, device,row):
        self._defaultcolor = parent.cget('bg')
        self._device = device
        self._text = device.device
        self._icon = PhotoImage(file='%s/%s'%(_imagepath,'mc.gif'))
        Button.__init__(self, master=parent, image=self._icon,
                        text=self._text, compound='left')
        self.grid(padx=10,pady=10, column=0, stick='ew')
        self.bind("<Button-1>",self.onClick)
        self.master.grid_columnconfigure(0, minsize=280)

    @property
    def device(self):
        return self._device

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = None
        self._icon = PhotoImage(file='%s/%s' % (_imagepath, value))

    @property
    def text(self):
        return self._text

    def onClick(self, event):
        self.master.master.master.dataframe = DataFrame(self.master.master.master, event.widget.device)
        self.master.master.master.storageframe= StorageFrame(self.master.master.master, event.widget.device)
        # reset the bg of all mediumchanger buttons
        for mediumchanger in self.master.master.widgets:
            mediumchanger.config(bg=self._defaultcolor)
        # set the bg of the clicked button
        self.config(bg='lightgreen')
