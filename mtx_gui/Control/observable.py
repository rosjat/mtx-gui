# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import logging

modul_logger = logging.getLogger("mtx-gui.control.observable")


class Observable(object):
    def __init__(self, view=None, model=None):
        self._view = view
        self._model = model
        self.callbacks = {}
        self.application_callback = None

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.view)
            func(self.model)

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value
        self._docallbacks()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value
        self._docallbacks()


class MediumChangerObserver(Observable):
    def onLeftClick(self, event):
        self.view.config(bg="lightblue")
        to_do = {
            "sender": self,
            "event": event,
            "action": "init",
        }
        self.application_callback(to_do)

    def onRightClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "contextmenu",
        }
        self.application_callback(to_do)

    def do_command(self, sender, event, cmd):
        if cmd == "load":
            self.model.load(sender.model.element_address, event.model.element_address)
        if cmd == "unload":
            self.model.unload(sender.model.element_address, event.model.element_address)


class StorageSlotObserver(Observable):
    def onLeftClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "init",
        }
        self.application_callback(to_do)

    def onRightClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "contextmenu",
        }
        self.application_callback(to_do)

    def onMenuLeftClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "unload",
        }
        self.application_callback(to_do)


class DataSlotObserver(Observable):
    def onLeftClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "init",
        }
        self.application_callback(to_do)

    def onRightClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "contextmenu",
        }
        self.application_callback(to_do)

    def onMenuLeftClick(self, event):
        modul_logger.debug(event.model.element_address)
        modul_logger.debug("sender: %s event: %s" % (self, event))
        to_do = {
            "sender": self,
            "event": event,
            "action": "load",
        }
        self.application_callback(to_do)


class DataSlotMenuObserver(Observable):
    def onLeftClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "init",
        }
        self.application_callback(to_do)


class StorageSlotMenuObserver(Observable):
    def onLeftClick(self, event):
        to_do = {
            "sender": self,
            "event": event,
            "action": "init",
        }
        self.application_callback(to_do)
