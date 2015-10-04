# coding: utf-8
"""collection of the widgets that are used in the View"""
from tkinter import Frame, Canvas
from mtx_gui.View.widgets.button import MediumChangerButton
from mtx_gui.View.widgets.label import DataLabel, StorageLabel
from mtx_gui.View.widgets.scrollbar import AutoScrollbar


class ScrollFrame(Frame):

    def __init__(self, parent, medium_changers=None, device=None):
        Frame.__init__(self, master=parent)
        # init all the stuff we need later on
        self._widgets = None
        self._medium_changers = medium_changers
        self._device = device
        # trick part, get this damn thing scrolling in the right place
        self.grid(stick='nsew')
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.config(height= 380, width= 300)
        self.grid_propagate(0)
        # with a little help, preparing the scrollbar. The final setup happens
        # in the special Slot Class
        self._sbar = AutoScrollbar(self)
        self._sbar.grid(row=0, column=1, stick='ns')
        self._canv = Canvas(self, yscrollcommand=self._sbar.set)
        self._canv.grid(row=0, column=0, stick='nswe')
        self._sbar.config(command=self._canv.yview)
        self.createWidgets()

    @property
    def device(self):
        return self._device

    @property
    def canv(self):
        return self._canv

    @property
    def sbar(self):
        return self._sbar

    @property
    def mediumchangers(self):
        return self._medium_changers

    @property
    def widgets(self):
        return self._widgets

    @widgets.setter
    def widgets(self, value):
        self._widgets = value

    @classmethod
    def createWidgets(cls):
        print('if you see this you did it wrong !!!')


class ChangerFrame(ScrollFrame):

    def __init__(self, parent, medium_changers):
        ScrollFrame.__init__(self, parent, medium_changers=medium_changers)
        self.grid(row=0,column=0)

    def createWidgets(self):
        """creating all the widgets in the main window"""
        if self.mediumchangers:
            # init the buttons for the medium
            counter = 0
            tmp = []
            for mc in self.mediumchangers:
                b = MediumChangerButton(self.canv, mc, counter)
                tmp.append(b)
                b = None
                counter +=1
            self.widgets = tmp


class StorageFrame(ScrollFrame):

    def __init__(self, parent, device):
        ScrollFrame.__init__(self, parent, device=device)
        self.grid(row=0, column=2)

    def createWidgets(self):

        if self.widgets:
            for label in self.widgets:
                label.update()
        else:
            labels =[]
            f = Frame(self.canv)
            f.rowconfigure(0, weight=1)
            f.columnconfigure(0, weight=1)
            for slot in self.device.storage_slots:
                label = StorageLabel(f,slot)
                labels.append(label)

            self.canv.create_window(0, 0, anchor='nw', window=f)
            f.update_idletasks()
            self.canv.config(scrollregion=self.canv.bbox("all"))
            self.widgets = labels


class DataFrame(ScrollFrame):

    def __init__(self, parent, device):
        ScrollFrame.__init__(self, parent, device=device)
        self.grid(row=0, column=1)

    def createWidgets(self):
        if self.widgets:
            for label in self.widgets:
                label.update()
        else:
            labels =[]
            for slot in self.device.data_slots:
                label = DataLabel(self.canv, slot)
                labels.append(label)
            self.widgets = labels