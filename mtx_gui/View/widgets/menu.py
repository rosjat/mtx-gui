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
"""collection of the widgets that are used in the View"""
import logging
from tkinter import Menu

modul_logger = logging.getLogger('mtx-gui.view.widgets.menu')


class DataSlotMenu(Menu):

    def __init__(self, parent, slots, **kwargs):
        Menu.__init__(self, parent, kwargs)
        for sl in slots:
            s = sl['primary_volume_tag'].decode(encoding="utf-8", errors="strict").replace('\x00', '').replace(' ', '')
            if s == '':
                modul_logger.debug('%s is empty' % s)
                self.add_command(label=u'unload to %s' % s, value=sl)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.grab_release()


class StorageSlotMenu(Menu):

    def __init__(self, parent, slots, **kwargs):
        Menu.__init__(self, parent, kwargs)
        for sl in slots:
            s = sl['primary_volume_tag'].decode(encoding="utf-8", errors="strict").replace('\x00', '').replace(' ', '')
            modul_logger.debug('-%s-' % s)
            if s == '':
                modul_logger.debug('%s is not empty' % s)
                self.add_command(label=u'load to %s' % s, value=sl)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.grab_release()
