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
__all__ = ['DataSlot', 'StorageSlot']
import logging

modul_logger = logging.getLogger('mtx-gui.model.slot')

class Slot(object):
    """
        class to collect the Information of a storage slot of a  medium changer
    """
    def __init__(self, slot):
        """
         :param device: reference to the medium changer were the slot belong to
         :param name : name of the storage slot element
         :param status: indicate if the slot is empty or holds a media
         :param slot: reference to the position of the slot in the medium changer
         :param volumetag: reference to the name of the media that is stored in this
                      slot

        """

        for key in slot.keys():
            try:
                p = getattr(Slot, key)
                p.fset(self, slot[key])
            except AttributeError as ex:
                setattr(self, '_' + key, slot[key])
            finally:
                if key != 'except':
                    p = getattr(Slot, key)
                    p.fset(self, slot[key])
                else:
                    self.Expect = slot[key]
            modul_logger.debug('%s is set to: %s' % (key, p.fget(self)))

    @property
    def name(self):
        """
            read only property for the _name variable

           :return: string

        """
        return self._name

    @name.setter
    def name(self, value):
        """
            setter for the _name variable

           :param value: the new value of the _name variable
           :return: string

        """
        self._name = value

    @property
    def status(self):
        """
            read only property for the _status variable

           :return: string

        """
        return self._status

    @status.setter
    def status(self, value):
        """
            setter for the _status variable

            :param value: the new value of the _status variable
            :return: string

        """
        self._status = value

    @property
    def slot(self):
        """
            read only property for the _slot variable

           :return: integer

        """
        return self._slot

    @slot.setter
    def slot(self, value):
        """
            setter for the _slot variable

            :param value: the new value of the _slot variable
            :return: integer

        """
        self._slot = int(value)

    @property
    def primary_volume_tag(self):
        """
            read only property for the _voltag variable

            :return: string

        """
        return self._primary_volume_tag

    @primary_volume_tag.setter
    def primary_volume_tag(self, value):
        """
            setter for the _voltag variable

            :param value: the new value of the _voltag variable
            :return: string

        """
        v = value.decode(encoding="utf-8", errors="strict").replace('\x00', '').replace(' ', '')
        self._primary_volume_tag = v

    @property
    def full(self):
        return self._full

    @full.setter
    def full(self, value):
        self._full = int(value)

    @property
    def invert(self):
        return self._invert

    @invert.setter
    def invert(self, value):
        self._invert = int(value)

    @property
    def element_address(self):
        return self._element_address

    @element_address.setter
    def element_address(self, value):
        self._element_address = int(value)

    @property
    def access(self):
        return self._access

    @access.setter
    def access(self, value):
        self._access = int(value)

    @property
    def source_storage_element_address(self):
        return self._source_storage_element_address

    @source_storage_element_address.setter
    def source_storage_element_address(self, value):
        self._source_storage_element_address = int(value)

    @property
    def additional_sense_code_qualifier(self):
        return self._additional_sense_code_qualifier

    @additional_sense_code_qualifier.setter
    def additional_sense_code_qualifier(self, value):
        self._additional_sense_code_qualifier = int(value)

    @property
    def additional_sense_code(self):
        return self._additional_sense_code

    @additional_sense_code.setter
    def additional_sense_code(self, value):
        self._additional_sense_code = int(value)

    @property
    def Except(self):
        return self._except

    @Except.setter
    def Except(self, value):
        self._except = int(value)

    @property
    def medium_type(self):
        return self._medium_type

    @medium_type.setter
    def medium_type(self, value):
        self._medium_type = int(value)

    @property
    def svalid(self):
        return self._svalid

    @svalid.setter
    def svalid(self, value):
        self._svalid = int(value)

    @property
    def ed(self):
        return self._ed

    @ed.setter
    def ed(self, value):
        self._ed = int(value)


class DataSlot(Slot):
    pass


class StorageSlot(Slot):
    pass

