# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later
"""handle the main window of the View"""
import logging
from tkinter import Frame

modul_logger = logging.getLogger("mtx-gui.view.Mainwindow")


class MainWindow(Frame):

    _version = "0.1"

    def __init__(self, master=None):
        """init the Frame instance"""
        try:
            Frame.__init__(self, master)
            self.init()
        except Exception as ex:
            modul_logger.error(ex)

    def init(self):
        self.master.title("mtx-gui version %s" % self._version)
        self.grid(stick="EWSN")
        self.grid_propagate(1)
        self.columnconfigure(0, weight=1)
