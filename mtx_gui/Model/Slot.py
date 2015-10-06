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
        self._slot = slot
        self._voltag = slot['primary_volume_tag'][0:32]
        self._status = slot['full']

    @property
    def device(self):
        """
            read only property for the _device variable

           :return: string

        """
        return self._device

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
    def volumetag(self):
        """
            read only property for the _voltag variable

            :return: string

        """
        return self._voltag

    @volumetag.setter
    def volumetag(self, value):
        """
            setter for the _voltag variable

            :param value: the new value of the _voltag variable
            :return: string

        """
        self._voltag = value


class DataSlot(Slot):
    pass


class StorageSlot(Slot):
    pass

