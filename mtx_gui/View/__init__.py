# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""collection of the widgets that are used in the View"""
from os import path
from tkinter import Tk, messagebox

# remember the image folder
_imagepath = path.join(path.split(path.dirname(__file__))[0], "View/img")


def create_tk_root():
    root = Tk()
    root.grid_propagate(1)
    root.resizable(0, 0)
    return root


def start_tk_gui(root):
    try:
        root.mainloop()
    except Exception as e:
        messagebox.showinfo(title="mtxgui info", message=str(e))
