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
"""handle the main window of the View"""
import logging
from tkinter import Frame

modul_logger = logging.getLogger('mtx-gui.view.Mainwindow')


class MainWindow(Frame):

    _version = '0.1'

    def __init__(self, master=None):
        """init the Frame instance"""
        try:
            Frame.__init__(self, master)
            self.init()
        except Exception as ex:
            modul_logger.error(ex)

    def init(self):
        self.master.title("mtx-gui version %s" % self._version)
        self.grid(stick='EWSN')
        self.grid_propagate(1)
        self.columnconfigure(0, weight=1)
