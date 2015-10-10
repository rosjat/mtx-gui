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

import os
import subprocess
import logging
from glob import glob

from mtx_gui.Model.MediumChanger import MediumChanger
from mtx_gui.Model.Slot import StorageSlot, DataSlot
from mtx_gui.Control.observable import MediumChangerObserver, StorageSlotObserver, DataSlotObserver

modul_logger = logging.getLogger('mtx-gui.control.api')

_scsi_devs = glob('/dev/sg*')


def check_root():
    if os.getuid() == 0:
        return True
    else:
        return False


def get_mtx_path():
    result = subprocess.getoutput('which mtx')
    return result


def get_devices():
    return [MediumChangerObserver(model=MediumChanger(dev)) for dev in _scsi_devs]


def get_storage_slots(mc):
    return [StorageSlotObserver(model=StorageSlot(slot)) for slot in mc.model.storage_slots]


def get_data_slots(mc):
    return [DataSlotObserver(model=DataSlot(slot)) for slot in mc.model.data_slots]
