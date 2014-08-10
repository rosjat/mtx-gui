# coding: utf-8

import os
import commands
from Changers.MediumChanger import MediumChanger as mc

def check_root():
    if os.getuid() == 0:
        return True
    else:
        return False

def get_medium_changers():
    temp = []
    result = commands.getoutput('sg_map').split('\n')
    for item in result:
        if item.find(' ') != -1:
            key, value = item.split()
            if is_medium_changer(key):
                temp.add(mc(key))
        else:
            if is_medium_changer(item):
                temp.append(mc(item))
    return temp

def is_medium_changer(devicename):
        cmd = 'sg_inq %s' % devicename
        result = commands.getoutput(cmd)
        if result.find('medium changer',0) != -1:
            return True
        else:
            return False