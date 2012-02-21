# coding: utf-8

import os
import commands

from slots import DataSlot, StorageSlot

class ScsiChanger(object):

    _sg_inq_query = '/usr/bin/sg_inq %s'
    _mtx_status_query = '/usr/sbin/mtx -f %s status'
    _mtx_load_query = '/usr/sbin/mtx -f %s load %s'
    _mtx_unload_query = '/usr/sbin/mtx -f %s unload %s'

    _queries = [_sg_inq_query, _mtx_status_query,
                _mtx_load_query, _mtx_unload_query,]

    _inquiry_values = ['Product revision level',
                       'Product identification',
                       'Vendor identification',
                       'Unit serial number',]

    @property
    def inquiry_data(self):
        return self._inquiry_data

    @property
    def device(self):
        return self._device

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, value):
        self._loaded = value

    @property
    def device_type(self):
        return self._device_type

    @staticmethod
    def query(self,query,slot=None):
        if query in self._queries:
            if slot:
                cmd = query % (self.device, slot)
            else:
                cmd = query % self.device
            result = commands.getoutput(cmd).split('\n')
            return result
        return '< invalid query >'

    @staticmethod
    def get_inquiry_data(cls):
        tmp = {}
        result = cls.query(cls,cls._sg_inq_query)
        for line in result:
            l = line.lstrip()
            if l.find(':') != -1:
                key, value = l.split(':')
                if key in cls._inquiry_values:
                    tmp[key] = value.lstrip()
    @staticmethod
    def load(cls, slot):
        result = ScsiChanger.query(cls,ScsiChanger._mtx_load_query,slot)
        if result[0].find('done') != -1:
            cls.loaded = slot
        return result

    @staticmethod
    def unload(cls, to_slot):
        if to_slot:
            result = ScsiChanger.query(cls,ScsiChanger._mtx_unload_query,to_slot)
        elif cls.loaded:
            result = ScsiChanger.query(cls,ScsiChanger._mtx_unload_query,to_slot)
        if result[0].find('done') != -1:
            cls.loaded = None
        return result

    @property
    def me(self):
        return self._me

    def __init__(self, device=None):
        self._loaded = None
        self._device = device
        self._me = self
        self._device_type = None
        self._inquiry_data = self.get_inquiry_data(self)

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