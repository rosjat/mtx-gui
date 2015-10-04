# coding: utf-8
import os
import subprocess
from glob import glob

from mtx_gui.Model.MediumChanger import MediumChanger
from mtx_gui.Control.observable import Observable

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
    return [Observable(MediumChanger(dev)) for dev in _scsi_devs]


