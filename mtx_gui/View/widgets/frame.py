# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
"""collection of the widgets that are used in the View"""
import logging
from tkinter import Frame, Canvas
from mtx_gui.View.widgets.label import DataLabel, StorageLabel
from mtx_gui.View.widgets.scrollbar import AutoScrollbar

modul_logger = logging.getLogger('mtx-gui.view.widgets.frame')


class ScrollFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, master=parent)
        # init all the stuff we need later on
        self._widgets = None
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

    @property
    def canv(self):
        return self._canv

    @property
    def sbar(self):
        return self._sbar

    @property
    def widgets(self):
        return self._widgets

    @widgets.setter
    def widgets(self, value):
        self._widgets = value


class StorageFrame(ScrollFrame):

    def __init__(self, parent, slots):
        ScrollFrame.__init__(self, parent)
        self.grid(row=0, column=2)
        labels = []
        f = Frame(self.canv)
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)
        for slot in slots:
            label = StorageLabel(f, slot)
            labels.append(label)
        self.canv.create_window(0, 0, anchor='nw', window=f)
        f.update_idletasks()
        self.canv.config(scrollregion=self.canv.bbox("all"))
        self.widgets = labels


class DataFrame(ScrollFrame):

    def __init__(self, parent, slots):
        ScrollFrame.__init__(self, parent)
        self.grid(row=0, column=1)
        labels = []
        for slot in slots:
            label = DataLabel(self.canv, slot)
            labels.append(label)
        self.widgets = labels
