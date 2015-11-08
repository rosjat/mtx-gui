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
from tkinter import Frame, Canvas, LabelFrame
from mtx_gui.View.widgets.label import DataLabel, StorageLabel
from mtx_gui.View.widgets.scrollbar import AutoScrollbar
from mtx_gui.View.widgets.button import MediumChangerButton

modul_logger = logging.getLogger('mtx-gui.view.widgets.frame')


class ScrollFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, master=parent)
        # init all the stuff we need later on
        self._widgets = None
        # trick part, get this damn thing scrolling in the right place
        self.grid(stick='nsew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # with a little help, preparing the scrollbar. The final setup happens
        # in the special Slot Class
        self._sbar = AutoScrollbar(self)
        self._sbar.grid(row=0, column=1, stick='ns')
        self._canv = Canvas(self, yscrollcommand=self._sbar.set)
        self._canv.config(bg='azure')
        self._canv.grid(row=0, column=0, stick='wens')
        self._sbar.config(command=self._canv.yview)
        self._canv.xview_moveto(0)
        self._canv.yview_moveto(0)
        self._content = Frame(self.canv)
        self._content.rowconfigure(0, weight=1, minsize=380)
        self._content.columnconfigure(0, weight=1)
        self._content_id = self.canv.create_window(0, 0, anchor='nw', window=self._content)
        self._content.bind('<Configure>', self._config_content)
        self.canv.bind('<Configure>', self._config_canv)
        self.grid_propagate(1)

    def _config_content(self, event):
        size = (self._content.winfo_reqwidth(), self._content.winfo_reqheight())
        self.canv.config(scrollregion='0 0 %s %s' % size)
        if self._canv.winfo_width() != self._content.winfo_reqwidth():
            self.canv.config(width=self._content.winfo_reqwidth())
        self.canv.itemconfigure(self._content_id, height=self.canv.winfo_height())

    def _config_canv(self, event):
        if self.canv.winfo_width() != self._content.winfo_reqwidth():
            self.canv.itemconfigure(self._content_id, width=self.canv.winfo_width())


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
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)
        self._content.config(padx=5, pady=5)
        group = LabelFrame(self._content, text="Storage Elements")
        group.grid(stick='NSEW')
        self._content.grid(row=0, column=0, stick='NSEW')
        for slot in slots:
            label = StorageLabel(group, slot)
            labels.append(label)
        self.canv.config(scrollregion=self.canv.bbox("all"))
        self.widgets = labels


class DataFrame(ScrollFrame):

    def __init__(self, parent, slots):
        ScrollFrame.__init__(self, parent)
        self.grid(row=0, column=1)
        labels = []
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)
        self._content.config(padx=5, pady=5)
        group = LabelFrame(self._content, text="Data Elements")
        group.grid(stick='NSEW')
        self._content.grid(row=0, column=0, stick='NSEW')
        for slot in slots:
            label = DataLabel(group, slot)
            labels.append(label)
        self.canv.config(scrollregion=self.canv.bbox("all"))
        self.widgets = labels


class MCFrame(ScrollFrame):

    def __init__(self, parent, app):
        ScrollFrame.__init__(self, parent)
        self.grid(row=0, column=0)
        buttons = []
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)
        self._content.config(padx=5, pady=5)
        group = LabelFrame(self._content, text="Data Elements")
        group.grid(stick='NSEW')
        self._content.grid(row=0, column=0, stick='NSEW')
        for mc in app.mediumchangers:
            mc.view = MediumChangerButton(group, mc)
            mc.application_callback = app.event_sink
            app.callbacks.update(mc.callbacks)
        self.canv.config(scrollregion=self.canv.bbox("all"))
        self.widgets = buttons
