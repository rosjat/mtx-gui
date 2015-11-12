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
from tkinter import Label, PhotoImage
from . import _imagepath

modul_logger = logging.getLogger('mtx-gui.view.widgets.label')


class SlotLabel(Label):
    """ Baseclass for the label widgets"""

    _icon = None
    _background = None
    _foreground = None
    _text = ''
    _default_bg_color = None
    _default_fg_color = None

    def __init__(self, parent, slot):
        try:
            Label.__init__(self,
                           parent,
                           justify='left',
                           anchor='w',
                           compound='left',
                           padx=20)
            self._init_properties(parent, slot)
            self._init_bindings(slot)
        except Exception as ex:
            modul_logger.error(ex)

    def _init_properties(self, parent, slot):
        """
            method to init some basic properties of the label

            :param parent: the parent widget of the the label
            :param slot: the slot observable
        """
        try:
            self.background = self._default_bg_color = parent.cget('bg')
            self.foreground = self._default_fg_color = parent.cget('fg')
            self._slot = slot
            self.text = ''
            self.icon = PhotoImage(file='%s/%s' % (_imagepath, 'storage.gif'))
            self.grid(padx=2,
                      pady=2,
                      stick='ew')
            self.master.grid_columnconfigure(0, minsize=300)
            self.grid_propagate(0)
        except Exception as ex:
            modul_logger.error(ex)

    def _init_bindings(self, slot):
        """
            method to init the binding to the callback methods in the observable

            :param slot: a slot observable
        """
        self.bind("<Button-1>", self._slot.onLeftClick)
        self.bind("<Button-3>", self._slot.onRightClick)


    @property
    def icon(self):
        """return the gif displayed with the label"""
        return self._icon

    @icon.setter
    def icon(self, value):
        """set the gif displayed with the label"""
        self._icon = value
        self.config(image=value)

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
        self.config(text=value)

    @property
    def background(self):
        """return the color for the label background"""
        return self._background

    @background.setter
    def background(self, value):
        """set the color for the label background"""
        self._background = value
        self.config(bg=value)

    @property
    def foreground(self):
        """return the color for the label background"""
        return self._background

    @foreground.setter
    def foreground(self, value):
        """set the color for the label background"""
        self._foreground = value
        self.config(fg=value)

    def menu_action(self, slot):
        print('if you see this you did it wrong !!!')

    def set_visuals(self):
        print('if you see this you did it wrong !!!')


class StorageLabel(SlotLabel):
    """class for the storage label"""
    def __init__(self, parent, slot):
        try:
            SlotLabel.__init__(self, parent, slot)
            if type(slot).__name__ != 'StorageSlotObserver':
                self.destroy()
            else:
                self.set_visuals()
        except Exception as ex:
            modul_logger.error(ex)

    def set_visuals(self):
        self.background = 'green'
        self.text = self.slot.model.primary_volume_tag
        if not self.slot.model.full:
            self.background = 'red'
            self.foreground = 'white'
            self.text = 'empty'

    def menu_action(self, slot):
        # self.slot.device.load(slot)
        # TODO: this cant be the final solution
        # self.master.master.master.master.statusbar.config(text=self.slot.device.last_msg)
        pass


class DataLabel(SlotLabel):
    """class for the data label"""
    def __init__(self, parent, slot):
        try:
            SlotLabel.__init__(self, parent, slot)
            if type(slot).__name__ != 'DataSlotObserver':
                self.destroy()
            else:
                self.set_visuals()
        except Exception as ex:
            modul_logger.error(ex)

    def set_visuals(self):
        self.text = self.slot.model.primary_volume_tag
        self.background = 'orange'
        if self.slot.model.full == 0:
            self.background = self._default_bg_color
            self.text = 'empty'

    def menu_action(self, slot):
        # self.slot.device.unload(slot)
        # TODO: this cant be the final solution
        # self.master.master.master.statusbar.config(text=self.slot.device.last_msg)
        pass


class StatusBar(Label):

    def __init__(self, parent):
        try:
            Label.__init__(self,
                           parent,
                           text='',
                           relief='sunken',
                           anchor='w')
            parent.master.stb = self
            self.grid(column=0,
                      columnspan=4,
                      sticky='ew')
            self._text = ''
        except Exception as ex:
            modul_logger.error(ex)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.config(text=value)
