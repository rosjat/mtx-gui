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
from pyscsi.pyscsi.scsi import SCSI

from mtx_gui.View import create_tk_root, start_tk_gui
from mtx_gui.View.MainWindow import MainWindow
from mtx_gui.View.widgets.frame import ChangerFrame
from mtx_gui.Control.api import *


class Application(object):
    """ the controller class for the application
    """
    def __init__(self):
        self._scsi = SCSI(None)
        self._mc = [mc for mc in get_devices() if self.is_medium_changer(mc)]
        self._main_gui = MainWindow(create_tk_root())

    @property
    def mediumchangers(self):
        return self._mc

    @property
    def gui(self):
        return self._main_gui

    def run(self):
        self.create_widgets()
        start_tk_gui(self.gui)

    def create_widgets(self):
        ChangerFrame(self.gui, self.mediumchangers)

    def is_medium_changer(self, dev):
        self._scsi(dev.data)
        # if self._scsi.inquiry().result['peripheral_device_type'] == 0x08:
        if self._scsi.inquiry().result['peripheral_device_type'] == 0x05:  # for testing we don't use the 8 as dev type
            return True
        return False

