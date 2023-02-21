# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later
"""collection of the widgets that are used in the View"""
import logging
from tkinter import Scrollbar, TclError

modul_logger = logging.getLogger("mtx-gui.view.widgets.scrollbar")


class AutoScrollbar(Scrollbar):
    """Autoscrollbar by Fredrik Lundh"""

    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        modul_logger.error(TclError("cannot use pack with this widget"))

    def place(self, **kw):
        modul_logger.error(TclError("cannot use place with this widget"))
