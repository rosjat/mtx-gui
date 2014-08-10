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
        cls.last_msg = result

    @staticmethod
    def unload(cls, to_slot):
        if to_slot:
            result = ScsiChanger.query(cls,ScsiChanger._mtx_unload_query,to_slot)
        elif cls.loaded:
            result = ScsiChanger.query(cls,ScsiChanger._mtx_unload_query,to_slot)
        if result[0].find('done') != -1:
            cls.loaded = None
        cls.last_msg = result

    @property
    def me(self):
        return self._me

    @property
    def last_msg(self):
        return self._last_msg

    @last_msg.setter
    def last_msg(self, value):
        self._last_msg = value

    def __init__(self, device=None):
        self._loaded = None
        self._device = device
        self._me = self
        self._device_type = None
        self._inquiry_data = self.get_inquiry_data(self)
        self._last_msg =''