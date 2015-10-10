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
from tkinter import Button, PhotoImage
from . import _imagepath

modul_logger = logging.getLogger('mtx-gui.view.widgets.button')

class MediumChangerButton(Button):
    """
        This class is the basic implementation for the a button widget that controls
        communication and visual representation  of the medium changer model
    """
    _icon = None
    _defaultcolor = None
    _text = ''

    def __init__(self, parent, mc):
        """
            Initialization of the widget and hooking op of callback methods

            :param parent: the parent widget
            :param mc: a medium changer observable instance
        """
        Button.__init__(self, master=parent, compound='left')
        self._init_properties(parent, mc)
        self._init_bindings(mc)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def text(self):
        return self._text

    def _init_properties(self, parent, mc):
        """
            method to init some basic properties of the button

            :param parent: the parent widget of the the button
            :param mc: the medium changer observable
        """
        self._defaultcolor = parent.cget('bg')
        self._text = mc.model.name
        self.icon = PhotoImage(file='%s/%s' % (_imagepath, 'mc.gif'))
        self.config(image=self.icon,
                    text=self._text, )
        self.master.grid_columnconfigure(0, minsize=280)
        self.grid(padx=10,
                  pady=10,
                  column=0,
                  stick='ew')

    def _init_bindings(self, mc):
        """
            method to init the binding to the callback methods in the observable

            :param mc: a medium changer observable
        """
        self.bind("<Button-1>", mc.onLeftClick)
        self.bind("<Button-3>", mc.onRightClick)
