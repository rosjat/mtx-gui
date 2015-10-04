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

from pyscsi.pyscsi.scsi_device import SCSIDevice


class MediumChanger(SCSIDevice):
    """
        Class to collect and manipulate medium changer data that is collected
        with the python-scsi package.
    """

    _storage_slots = None
    _data_slots = None

    def __init__(self, device=None):
        SCSIDevice.__init__(self, device)

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

    def get_storage_slots(self, result):
        pass

    def update(self, result):
        pass

    def get_data_slots(self, result):
        pass

    def load(self, slot):
        pass

    def unload(self, to_slot):
        pass