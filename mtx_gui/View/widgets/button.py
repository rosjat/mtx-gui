# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""collection of the widgets that are used in the View"""
import logging
from tkinter import Button, PhotoImage

from . import _imagepath

modul_logger = logging.getLogger("mtx-gui.view.widgets.button")


class MediumChangerButton(Button):
    """
    This class is the basic implementation for the a button widget that controls
    communication and visual representation  of the medium changer model
    """

    _icon = None
    _defaultcolor = None
    _text = ""
    _justify = ""

    def __init__(self, parent, mc):
        """
        Initialization of the widget and hooking op of callback methods

        :param parent: the parent widget
        :param mc: a medium changer observable instance
        """
        Button.__init__(self, master=parent, compound="left")
        self._init_properties(parent, mc)
        self._init_bindings(mc)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.config(image=value)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.config(text=value)

    @property
    def justify(self):
        return self._justify

    @justify.setter
    def justify(self, value):
        self._justify
        self.config(justify=value)

    def _init_properties(self, parent, mc):
        """
        method to init some basic properties of the button

        :param parent: the parent widget of the the button
        :param mc: the medium changer observable
        """
        self._defaultcolor = parent.cget("bg")
        inq = mc.model.inquiry().result
        self.text = "%s(%s)\r\n%s" % (
            inq["t10_vendor_identification"][:32]
            .decode(encoding="utf-8", errors="strict")
            .replace("\x00", ""),
            inq["product_identification"][:32]
            .decode(encoding="utf-8", errors="strict")
            .replace("\x00", ""),
            mc.model.name,
        )
        self.justify = "left"
        self.icon = PhotoImage(file="%s/%s" % (_imagepath, "mc.gif"))
        self.master.grid_columnconfigure(0, minsize=280)
        self.grid(padx=5, pady=5, column=0, stick="ew")

    def _init_bindings(self, mc):
        """
        method to init the binding to the callback methods in the observable

        :param mc: a medium changer observable
        """
        self.bind("<Button-1>", mc.onLeftClick)
        self.bind("<Button-3>", mc.onRightClick)
