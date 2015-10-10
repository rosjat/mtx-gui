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
from pyscsi.pyscsi.scsi_device import SCSIDevice
from pyscsi.pyscsi import scsi_enum_modesense as MODESENSE6
from pyscsi.pyscsi import scsi_enum_readelementstatus as READELEMENTSTATUS

modul_logger = logging.getLogger('mtx-gui.model.MediumChanger')

class MediumChanger(SCSI):
    """
        Class to collect and manipulate medium changer data that is collected
        with the python-scsi package.
    """

    _storage_slots = None
    _data_slots = None
    _name = None

    def __init__(self, device=None):
        try:
            SCSI.__init__(self, SCSIDevice(device))
            self._name = device
        except Exception as ex:
            modul_logger.error(ex)

    @property
    def name(self):
        return self._name

    @property
    def storage_slots(self):
        return self._storage_slots

    @storage_slots.setter
    def storage_slots(self, value):
        self._storage_slots = value

    @property
    def data_slots(self):
        return self._data_slots

    @data_slots.setter
    def data_slots(self, value):
        self._data_slots = value

    def get_storage_slots(self):
        try:
            eaa = self.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result['mode_pages'][0]
            se = self.readelementstatus(start=eaa['first_storage_element_address'],
                                        num=eaa['num_storage_elements'],
                                        element_type=READELEMENTSTATUS.ELEMENT_TYPE.STORAGE,
                                        voltag=1,
                                        curdata=1,
                                        dvcid=1,
                                        alloclen=16384).result['element_status_pages'][0]['element_descriptors']
            self.storage_slots = se
        except Exception as ex:
            modul_logger.error(ex)

    def update(self, result):
        pass

    def get_data_slots(self):
        try:
            eaa = self.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result['mode_pages'][0]
            dte = self.readelementstatus(start=eaa['first_data_transfer_element_address'],
                                         num=eaa['num_data_transfer_elements'],
                                         element_type=READELEMENTSTATUS.ELEMENT_TYPE.DATA_TRANSFER,
                                         voltag=1,
                                         curdata=1,
                                         dvcid=1,
                                         alloclen=16384).result['element_status_pages'][0]['element_descriptors']
            self.data_slots = dte
        except Exception as ex:
            modul_logger.error(ex)

    def load(self, slot):
        pass

    def unload(self, to_slot):
        pass

    def is_medium_changer(self):
        if self.inquiry().result['peripheral_device_type'] == 0x08:
            return True
        return False
