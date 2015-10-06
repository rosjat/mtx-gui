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

from functools import partial
from tkinter import Label, PhotoImage, Menu
from . import _imagepath


class SlotLabel(Label):
    """baseclass for the label widgets"""
    def __init__(self,parent, slot):

        self._defaultcolor = parent.cget('bg')
        self._slot = slot
        self._background = self._defaultcolor
        self._text = ''
        self._icon = PhotoImage(file='%s/%s'%(_imagepath,'storage.gif'))
        Label.__init__(self,
                       parent,
                       justify='left',
                       anchor='w',
                       image=self._icon,
                       text=self._text,
                       bg=self._background,
                       compound='left')
        self.grid(padx=2,
                  pady=2,
                  stick='ew')
        self.master.grid_columnconfigure(0, minsize=300)
        self.grid_propagate(0)
        self.bind("<Button-1>", slot.onLeftClick)

    @property
    def icon(self):
        """return the gif displayed with the label"""
        return self._icon

    @icon.setter
    def icon(self, value):
        """set the gif displayed with the label"""
        self._icon = None
        self._icon = PhotoImage(file='%s/%s' % (_imagepath, value))

    @property
    def slot(self):
        """return the slot from the media changer device that should be controled"""
        return self._slot

    @property
    def text(self):
        """return the text that is displayed with the label"""
        return self._text

    @text.setter
    def text(self, value):
        """set the text that is displayed on the label"""
        self._text = value

    @property
    def background(self):
        """return the color for the label background"""
        return self._background

    @background.setter
    def background(self, value):
        """set the color for the label background"""
        self._background = value

    def onRightClick(self, event):
        """handle the right click event"""
        print('if you see this you did it wrong !!!')

    def menu_action(self, slot):
        print('if you see this you did it wrong !!!')

    def set_visuals(self):
        print('if you see this you did it wrong !!!')


class StorageLabel(SlotLabel):
    """class for the storage label"""
    def __init__(self, parent, slot):
        if type(slot).__name__ != 'StorageSlotObserver':
            self.destroy()
        else:
            SlotLabel.__init__(self, parent, slot)
            self.set_visuals()

    def set_visuals(self):
        self.config(bg='green')
        self.config(text=self.slot.model.volumetag.decode(encoding="utf-8", errors="strict"))
        if not self.slot.model.status:
            self.config(bg='red')
            self.config(text='empty')
        self.update_idletasks()

    def onRightClick(self, event):
        """
        if self.slot.status == 'Full ':
            popup = Menu(self,tearoff=0)
            popup.add_command(label=u'load', command=partial(self.menu_action, self.slot.slot))
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup.grab_release()
                self.updated()
        """
        pass

    def menu_action(self, slot):
        # self.slot.device.load(slot)
        # TODO: this cant be the final solution
        # self.master.master.master.master.statusbar.config(text=self.slot.device.last_msg)
        pass


class DataLabel(SlotLabel):
    """class for the data label"""
    def __init__(self, parent, slot):
        if type(slot).__name__ != 'DataSlotObserver':
            self.destroy()
        else:
            SlotLabel.__init__(self, parent, slot)
            self.set_visuals()

    def set_visuals(self):
        self.config(text=self.slot.model.volumetag)
        self.config(bg='orange')
        if not self.slot.model.status:
            self.config(bg=self._defaultcolor)
            self.config(text='empty')
        self.update_idletasks()

    def onRightClick(self, event):
        """
        if self.slot.status != 'Empty':
            popup = Menu(self,tearoff=0)
            unloadmenu = Menu(self, tearoff=0)
            for slot in self.slot.device.storage_slots:
                if slot.status == 'Empty':
                    unloadmenu.add_command(label=u'storage slot %s' % slot.slot,
                                           command=partial(self.menu_action, slot.slot))
            popup.add_cascade(label='unload', menu=unloadmenu)
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup.grab_release()
                self.updated()
        """
        pass

    def menu_action(self, slot):
        # self.slot.device.unload(slot)
        # TODO: this cant be the final solution
        # self.master.master.master.statusbar.config(text=self.slot.device.last_msg)
        pass


class StatusBar(Label):

    def __init__(self, parent):
        Label.__init__(self, parent, text='', relief='sunken', anchor='w')
        parent.master.stb = self
        self.grid(column=0, columnspan=4, sticky='ew')
        self._text = ''

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.config(text=value)
