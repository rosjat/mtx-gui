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
from functools import partial

modul_logger = logging.getLogger('mtx-gui.view.widgets.menu')


class SlotMenu(Menu):

    def __init__(self, parent, source, slots, label_template, **kwargs):
        Menu.__init__(self, parent, kwargs)
        modul_logger.debug('1 -> init menu')
        for sl in slots:
            modul_logger.debug('2 -> %s' % sl)
            m = sl.model
            v = sl.view
            modul_logger.debug('3 -> tag: %s' % m.primary_volume_tag)
            if m.primary_volume_tag == '':
                modul_logger.debug('4 -> add command')
                self.add_command(label=label_template % m.element_address,
                                 command=partial(sl.onMenuLeftClick, source))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.grab_release()

