# -*- coding: utf-8 -*-
import subprocess
import time
from unittest import TestCase
from unittest import skip

from Model.MediumChanger import MediumChanger

mediumx = '/dev/sg14'


class TestMediumChanger(TestCase):
    '''
    The test code assumes hitting mhvtl simulated STK L80 medium changer

    '''
    mc = None

    @classmethod
    def setUpClass(cls):
        # let all drive slots empty and all storage slots full
        subprocess.run(["/etc/init.d/mhvtl", "shutdown"], timeout=10, check=True)
        subprocess.run(["/etc/init.d/mhvtl", "start"], timeout=10, check=True)
        time.sleep(5)

        cls.mc = MediumChanger(mediumx)

    def test_name(self):
        self.assertEqual(mediumx, self.mc.name)

    def test_storage_slots(self):
        self.mc.get_storage_slots()
        self.assertGreater(len(self.mc.storage_slots), 0)  # at least one slot

        # pprint(self.mc.storage_slots[0])
        '''
{'access': 1,
 'additional_sense_code': 0,
 'additional_sense_code_qualifier': 0,
 'ed': 0,
 'element_address': 1000,
 'except': 0,
 'full': 1,
 'invert': 0,
 'medium_type': 1,
 'primary_volume_tag': bytearray(b'G03001TA                            '),
 'source_storage_element_address': 0,
 'svalid': 0}
        '''

        self.assertIsNotNone(self.mc.storage_slots[0].get('primary_volume_tag'))
        self.assertIsNotNone(self.mc.storage_slots[0].get('element_address'))
        self.assertIsNotNone(self.mc.storage_slots[0].get('source_storage_element_address'))
        self.assertIsNotNone(self.mc.storage_slots[0].get('full'))

    def test_data_slots(self):
        self.mc.get_data_slots()
        self.assertGreater(len(self.mc.data_slots), 0)

        # pprint(self.mc.data_slots[0])
        '''
{'access': 1,
 'additional_sense_code': 0,
 'additional_sense_code_qualifier': 0,
 'ed': 0,
 'element_address': 500,
 'except': 0,
 'full': 0,
 'invert': 0,
 'medium_type': 0,
 'primary_volume_tag': bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00'),
 'source_storage_element_address': 0,
 'svalid': 0}
        '''

        self.assertIsNotNone(self.mc.data_slots[0].get('primary_volume_tag'))
        self.assertIsNotNone(self.mc.data_slots[0].get('element_address'))
        self.assertIsNotNone(self.mc.data_slots[0].get('source_storage_element_address'))
        self.assertIsNotNone(self.mc.data_slots[0].get('full'))

    def test_medium_transport_elements(self):
        self.mc.get_medium_transport_elements()
        self.assertGreater(len(self.mc.medium_transport_elements), 0)

        # pprint(self.mc.medium_transport_elements[0])
        '''
        {'additional_sense_code': 0,
 'additional_sense_code_qualifier': 0,
 'ed': 0,
 'element_address': 1,
 'except': 0,
 'full': 0,
 'invert': 0,
 'medium_type': 0,
 'primary_volume_tag': bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
                                 b'\x00\x00\x00\x00'),
 'source_storage_element_address': 0,
 'svalid': 0}
        '''

        # is these useful for medium transport element?
        self.assertIsNotNone(self.mc.medium_transport_elements[0].get('primary_volume_tag'))
        self.assertIsNotNone(self.mc.medium_transport_elements[0].get('element_address'))
        self.assertIsNotNone(self.mc.medium_transport_elements[0].get('source_storage_element_address'))
        self.assertIsNotNone(self.mc.medium_transport_elements[0].get('full'))

    @skip
    def test_get_storage_slots(self):
        self.fail()

    @skip
    def test_get_data_slots(self):
        self.fail()

    @skip
    def test_get_medium_transport_elements(self):
        self.fail()

    def test_load(self):
        subprocess.run(['mtx', '-f', mediumx, 'unload', '1', '0'], timeout=3, check=False)
        time.sleep(3)

        self.mc.get_data_slots()
        self.mc.get_storage_slots()
        self.mc.get_medium_transport_elements()

        # basic
        self.mc.load(500, 1000)  # the first data and storage slot

        self.mc.get_data_slots()
        self.mc.get_storage_slots()

        self.assertEqual(1, self.mc.data_slots[0].get('full'))
        self.assertEqual(0, self.mc.storage_slots[0].get('full'))

        # FIXME: cannot catch exception since pyscsi does not convert the exception into python one
        # already loaded
        # try:
        #     self.mc.load(500, 1000)
        # except:
        #     print("qq")

    def test_unload(self):
        subprocess.run(['mtx', '-f', mediumx, 'load', '1', '0'], timeout=3, check=False)
        time.sleep(3)

        self.mc.get_data_slots()
        self.mc.get_storage_slots()
        self.mc.get_medium_transport_elements()

        # basic
        self.mc.unload(500, 1000)  # the first data and storage slot

        self.mc.get_data_slots()
        self.mc.get_storage_slots()

        self.assertEqual(0, self.mc.data_slots[0].get('full'))
        self.assertEqual(1, self.mc.storage_slots[0].get('full'))

        # FIXME: cannot catch exception since pyscsi does not convert the exception into python one
        # already loaded
        # try:
        #     self.mc.unload(500, 1000)
        # except:
        #     print("qq")

    def test_is_medium_changer(self):
        self.assertTrue(MediumChanger(mediumx).is_medium_changer())
        self.assertFalse(MediumChanger('/dev/nst0').is_medium_changer())

    @skip
    def test_get_element_offsets(self):
        self.fail()
