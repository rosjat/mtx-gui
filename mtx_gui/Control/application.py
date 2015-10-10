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

from pyscsi.pyscsi.scsi import SCSI

from mtx_gui.View import create_tk_root, start_tk_gui
from mtx_gui.View.MainWindow import MainWindow
from mtx_gui.View.widgets.frame import ScrollFrame, DataFrame, StorageFrame
from mtx_gui.View.widgets.button import MediumChangerButton
from mtx_gui.Control.api import *
from mtx_gui.Control.observable import Observable

modul_logger = logging.getLogger('mtx-gui.control.application')


class Application(Observable):
    """ the controller class for the application
    """
    def __init__(self):
        super().__init__()
        self._scsi = SCSI(None)
        self._mc = [mc for mc in get_devices() if mc.model.is_medium_changer()]
        self.view = MainWindow(create_tk_root())
        self.model = self
        self._ds = {}
        self._ss = {}

    @property
    def mediumchangers(self):
        return self._mc

    def run(self):
        self.create_widgets()
        start_tk_gui(self.view)

    def create_widgets(self):
        """creating all the widgets in the main window"""
        sc = ScrollFrame(self.view)
        counter = 0
        for mc in self.mediumchangers:
            mc.view = MediumChangerButton(sc.canv, mc)
            mc.application_callback = self.event_sink
            self.callbacks.update(mc.callbacks)
            counter += 1

    def event_sink(self, callback_dict):
        sender = callback_dict['sender']
        event = callback_dict['event']
        action = callback_dict['action']
        # TODO: make this part less ugly by putting it in extra methods or functions
        if type(sender) == MediumChangerObserver and action == 'init':
            sender.model.get_data_slots()
            sender.model.get_storage_slots()
            self._ds.update({sender: get_data_slots(sender)})
            self._ss.update({sender: get_storage_slots(sender)})
            StorageFrame(self.view, self._ss[sender])
            DataFrame(self.view, self._ds[sender])
            for s in self._ss[sender]:
                s.application_callback = self.event_sink
            for s in self._ds[sender]:
                s.application_callback = self.event_sink
        if type(sender) == StorageSlotObserver and action == 'init':
            print('storage Slot - left mouse button')


