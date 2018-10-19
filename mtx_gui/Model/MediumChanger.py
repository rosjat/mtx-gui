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
    def __init__(self, device=None):
        self._storage_slots = None
        self._data_slots = None
        self._medium_transport_elements = None
        self._name = None
        
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

    @property
    def medium_transport_elements(self):
        return self._medium_transport_elements

    @medium_transport_elements.setter
    def medium_transport_elements(self, value):
        self._medium_transport_elements = value

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

    def get_medium_transport_elements(self):
        try:
            eaa = self.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result['mode_pages'][0]
            mte = self.readelementstatus(start=eaa['first_medium_transport_element_address'],
                                         num=eaa['num_medium_transport_elements'],
                                         element_type=READELEMENTSTATUS.ELEMENT_TYPE.MEDIUM_TRANSPORT,
                                         voltag=1,
                                         curdata=1,
                                         dvcid=1,
                                         alloclen=16384).result['element_status_pages'][0]['element_descriptors']
            self.medium_transport_elements = mte
        except Exception as ex:
            modul_logger.error(ex)

    def load(self, data_transfer_element, storage_element):
        _fmte, _fdte, _fse = self.get_element_offsets(self.medium_transport_elements,
                                                      self.data_slots,
                                                      self.storage_slots)
        modul_logger.debug('dte: %s se: %s' % (data_transfer_element, storage_element))
        modul_logger.debug('_fmte: %s _fdte: %s _fse: %s' % (_fmte, _fdte, _fse))
        r = self.movemedium(_fmte,
                            storage_element,
                            data_transfer_element).result
        modul_logger.debug(r)

    def unload(self, data_transfer_element, storage_element):
        _fmte, _fdte, _fse = self.get_element_offsets(self.medium_transport_elements,
                                                      self.data_slots,
                                                      self.storage_slots)
        r = self.movemedium(_fmte,
                            data_transfer_element + _fdte,
                            storage_element + _fse - _fdte).result
        modul_logger.debug(r)

    def is_medium_changer(self):
        if self.inquiry().result['peripheral_device_type'] == 0x08:
            return True
        return False

    def get_element_offsets(self, mte, dte, se):
        _fmte = 99999999
        for element in mte:
            if element['element_address'] < _fmte:
                _fmte = element['element_address']
        _fdte = 99999999
        for element in dte:
            if element['element_address'] < _fdte:
                _fdte = element['element_address']
        _fse = 99999999
        for element in se:
            if element['element_address'] < _fse:
                _fse = element['element_address']
        return _fmte, _fdte, _fse
