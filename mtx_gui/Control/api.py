# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import logging
import os
import subprocess
from glob import glob

from Control.observable import (
    DataSlotObserver,
    MediumChangerObserver,
    StorageSlotObserver,
)
from Model.MediumChanger import MediumChanger
from Model.Slot import DataSlot, StorageSlot

modul_logger = logging.getLogger("mtx-gui.control.api")

_scsi_devs = glob("/dev/sg*")


def check_root():
    if os.getuid() == 0:
        return True
    else:
        return False


def get_mtx_path():
    result = subprocess.getoutput("which mtx")
    return result


def get_devices():
    return [MediumChangerObserver(model=MediumChanger(dev)) for dev in _scsi_devs]


def get_storage_slots(mc):
    return [
        StorageSlotObserver(model=StorageSlot(slot)) for slot in mc.model.storage_slots
    ]


def get_data_slots(mc):
    return [DataSlotObserver(model=DataSlot(slot)) for slot in mc.model.data_slots]
