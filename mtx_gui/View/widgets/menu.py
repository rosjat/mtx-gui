# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later
"""collection of the widgets that are used in the View"""
import logging
from functools import partial
from tkinter import Menu

modul_logger = logging.getLogger("mtx-gui.view.widgets.menu")


class SlotMenu(Menu):
    def __init__(self, parent, source, slots, label_template, **kwargs):
        Menu.__init__(self, parent, kwargs)
        modul_logger.debug("1 -> init menu")
        for sl in slots:
            modul_logger.debug("2 -> %s" % sl)
            m = sl.model
            v = sl.view
            modul_logger.debug("3 -> tag: %s" % m.primary_volume_tag)
            if m.primary_volume_tag == "":
                modul_logger.debug("4 -> add command")
                self.add_command(
                    label=label_template % m.element_address,
                    command=partial(sl.onMenuLeftClick, source),
                )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.grab_release()
