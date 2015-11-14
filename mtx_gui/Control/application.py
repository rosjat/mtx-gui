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
from mtx_gui.View import create_tk_root, start_tk_gui
from mtx_gui.View.MainWindow import MainWindow
from mtx_gui.View.widgets.frame import MCFrame, DataFrame, StorageFrame
from mtx_gui.View.widgets.menu import SlotMenu
from mtx_gui.Control.api import *
from mtx_gui.Control.observable import Observable

modul_logger = logging.getLogger('mtx-gui.control.application')


class Application(Observable):
    """ the controller class for the application
    """
    def __init__(self):
        super().__init__()
        self._mc = [mc for mc in get_devices() if mc.model.is_medium_changer()]
        self.view = MainWindow(create_tk_root())
        self.model = self
        self._ds = {}
        self._ss = {}
        self._widgets = []

    @property
    def mediumchangers(self):
        return self._mc

    def run(self):
        self.create_widgets()
        start_tk_gui(self.view)

    def create_widgets(self):
        """creating all the widgets in the main window"""
        self._widgets.append(MCFrame(self.view, self))

    def event_sink(self, callback_dict):
        sender = callback_dict['sender']
        event = callback_dict['event']
        action = callback_dict['action']
        if type(sender) == MediumChangerObserver and action == 'init':
            self._init_medium_changer_button(sender)
        if type(sender) == StorageSlotObserver:
            modul_logger.debug('storageslot')
            if action == 'contextmenu':
                self._init_storage_slot_contextmenu(sender, event)
            if action == 'unload':
                self._init_mc_command(sender, event, 'unload')
        if type(sender) == DataSlotObserver:
            modul_logger.debug('dataslot')
            if action == 'contextmenu':
                self._init_data_slot_contextmenu(sender, event)
            if action == 'load':
                modul_logger.debug('sender: %s event: %s' % (sender, event))
                self._init_mc_command(sender, event, 'load')

    def _init_medium_changer_button(self, sender):
        # issue a modesense + elementstatus
        sender.model.get_medium_transport_elements()
        sender.model.get_data_slots()
        sender.model.get_storage_slots()
        # now take the collected data and wrap it in nice Slot objects
        self._ds.update({sender: get_data_slots(sender)})
        self._ss.update({sender: get_storage_slots(sender)})
        StorageFrame(self.view, self._ss[sender])
        DataFrame(self.view, self._ds[sender])
        for s in self._ss[sender]:
            s.application_callback = self.event_sink
        for s in self._ds[sender]:
            s.application_callback = self.event_sink

    def _init_storage_slot_contextmenu(self, sender, event):
        mc = [k for k, v in self._ss.items() if sender in v][0]
        with SlotMenu(sender.view,
                      sender,
                      self._ds[mc],
                      u'load to %s',
                      tearoff=0) as popup:
            modul_logger.debug('text: %s' % sender.view.text)
            if sender.view.text != 'empty':
                modul_logger.debug('show ss contextmenu')
                popup.tk_popup(event.x_root, event.y_root, 0)

    def _init_data_slot_contextmenu(self, sender, event):
        mc = [k for k, v in self._ds.items() if sender in v][0]
        with SlotMenu(sender.view,
                      sender,
                      self._ss[mc],
                      u'unload to %s',
                      tearoff=0) as popup:
            modul_logger.debug('text: %s' % sender.view.text)
            if sender.view.text != 'empty':
                modul_logger.debug('show ds contextmenu')
                popup.tk_popup(event.x_root, event.y_root, 0)

    def _init_mc_command(self, sender, event, cmd):
        mc = [k for k, v in self._ds.items() if sender in v][0]
        mc.do_command(sender, event, cmd)
