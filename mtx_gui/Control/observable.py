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
import logging

modul_logger = logging.getLogger('mtx-gui.control.observable')


class Observable(object):

    def __init__(self, view=None, model=None):
        self._view = view
        self._model = model
        self.callbacks = {}
        self.application_callback = None

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.view)
            func(self.model)

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value
        self._docallbacks()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value
        self._docallbacks()


class MediumChangerObserver(Observable):

    def onLeftClick(self, event):
        self.view.config(bg='lightblue')
        to_do = {'sender': self,
                 'event': event,
                 'action': 'init', }
        self.application_callback(to_do)

    def onRightClick(self, event):
        to_do = {'sender': self,
                 'event': event,
                 'action': 'contextmenu', }
        self.application_callback(to_do)


class StorageSlotObserver(Observable):

    def onLeftClick(self, event):
        to_do = {'sender': self,
                 'event': event,
                 'action': 'init', }
        self.application_callback(to_do)

    def onRightClick(self, event):
        to_do = {'sender': self,
                 'event': event,
                 'action': 'contextmenu', }
        self.application_callback(to_do)


class DataSlotObserver(Observable):

    def onLeftClick(self, event):
        to_do = {'sender': self,
                 'event': event,
                 'action': 'init', }
        self.application_callback(to_do)

    def onRightClick(self, event):
        to_do = {'sender': self,
                 'event': event,
                 'action': 'contextmenu', }
        self.application_callback(to_do)


class DataSlotMenuObserver(Observable):

    def onLeftClick(self, event):
        to_do = {'sender': self,
                 'event': event,
                 'action': 'init', }
        self.application_callback(to_do)


class StorageSlotMenuObserver(Observable):

    def onLeftClick(self, event):
        to_do = {'sender': self,
                 'event': event,
                 'action': 'init', }
        self.application_callback(to_do)
