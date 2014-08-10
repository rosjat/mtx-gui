# coding: utf-8

import os
import commands

from slots import DataSlot, StorageSlot

class MediumChanger(ScsiChanger):
    '''Class to collect and manipulate medium cahnger data that is collected
       with the mtx tool.

    '''
    def __init__(self, device=None):
        ScsiChanger.__init__(self, device)
        self._device_type = 'medium changer'
        self._storage_slots = self.get_storage_slots(
                         ScsiChanger.query(self,ScsiChanger._mtx_status_query))
        self._data_slots = self.get_data_slots(
                         ScsiChanger.query(self,ScsiChanger._mtx_status_query))
    @property
    def storage_slots(self):
        return self._storage_slots

    @property
    def data_slots(self):
        return self._data_slots

    def get_storage_slots(self, result):
        tmp =[]
        for item in result:
            if item.find('Storage Element') != -1 and item.find('Data') == -1:
                    name, status, volumeinfo = item.split(':')
                    volumeinfo = volumeinfo.partition('=')
                    storageslot = StorageSlot(self.me,name.lstrip(),status,
                                    name.split()[2],volumeinfo[2].rstrip())
                    tmp.append(storageslot)
        return tmp

    def update(self, result):
        for item in result:
            if item.find('Data Transfer Element') != -1 \
                and item.find('Full') == -1:
                    name, status = item.split(':')
                    for slot in self.data_slots:
                        if name.lstrip() == slot.name:
                            slot.status = status
                            slot.volumetag = None
            elif item.find('Data Transfer Element') != -1 \
                 and item.find('Full') != -1:
                name, status, volumeinfo = item.split(':')
                volumeinfo = volumeinfo.partition('=')
                for slot in self.data_slots:
                        if name.lstrip() == slot.name:
                            slot.status = status,
                            slot.volumetag = volumeinfo[2].rstrip()
            elif item.find('Storage Element') != -1 and item.find('Data') == -1:
                name, status, volumeinfo = item.split(':')
                for slot in self.storage_slots:
                    if name.lstrip() == slot.name:
                        volumeinfo = volumeinfo.partition('=')
                        slot.status = status
                        slot.volumetag = volumeinfo[2].rstrip()

    def get_data_slots(self,result):
        tmp =[]
        for item in result:
            if item.find('Data Transfer Element') != -1 \
                and item.find('Full') == -1:
                    name, status = item.split(':')
                    dataslot = DataSlot(self.me,name.lstrip(),
                                        status, name.split()[3])
                    tmp.append(dataslot)

            elif item.find('Data Transfer Element') != -1 \
                 and item.find('Full') != -1:
                name, status, volumeinfo = item.split(':')
                volumeinfo = volumeinfo.partition('=')
                dataslot = DataSlot(self.me, name.lstrip(),
                                    status,status.split()[3],
                                    volumeinfo[2].rstrip())
                tmp.append(dataslot)
                self.loaded = dataslot.slot
        return tmp

    def load(self,slot):
        ScsiChanger.load(self,slot)
        self.update(ScsiChanger.query(self,ScsiChanger._mtx_status_query))

    def unload(self,to_slot):
        ScsiChanger.unload(self,to_slot)
        self.update(ScsiChanger.query(self,ScsiChanger._mtx_status_query))