# coding: utf-8

class StorageSlot(object):
    '''class to collect the Information of a storage slot of a  medium changer
    '''
    def __init__(self, device, name=None , status=None,
                                           slot=None, volumetag=None):
        '''
         :param device: reference to the medium changer were the slot belong to
         :param name : name of the storage slot element
         :param status: indicate if the slot is empty or holds a media
         :param slot: reference to the position of the slot in the medium changer
         :param volumetag: reference to the name of the media that is stored in this
                      slot

        '''
        self._name = name
        self._status = status
        self._slot = slot
        self._voltag = volumetag
        self._device = device

    @property
    def device(self):
        '''read only property for the _device variable

           :return: string

        '''
        return self._device

    @property
    def name(self):
        '''read only property for the _name variable

           :return: string

        '''
        return self._name

    @name.setter
    def name(self, value):
        '''setter for the _name variable

           :param value: the new value of the _name variable
           :return: string

        '''
        self._name = value

    @property
    def status(self):
        '''read only property for the _status variable

           :return: string

        '''
        return self._status

    @status.setter
    def status(self, value):
        '''setter for the _status variable

           :param value: the new value of the _status variable
           :return: string

        '''
        self._status = value

    @property
    def slot(self):
        '''read only property for the _slot variable

           :return: integer

        '''
        return self._slot

    @slot.setter
    def slot(self, value):
        '''setter for the _slot variable

           :param value: the new value of the _slot variable
           :return: integer

        '''
        self._slot = int(value)

    @property
    def volumetag(self):
        '''read only property for the _voltag variable

           :return: string

        '''
        return self._voltag

    @volumetag.setter
    def volumetag(self, value):
        '''setter for the _voltag variable

           :param value: the new value of the _voltag variable
           :return: string

        '''
        self._voltag = value
