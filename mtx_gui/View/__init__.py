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
from os import path
from tkinter import Tk, messagebox
# remember the image folder
_imagepath = path.join(path.split(path.dirname(__file__))[0], 'View/img')


def create_tk_root():
    root = Tk()
    root.config(height=400)
    root.grid_propagate(1)
    root.resizable(0, 0)
    return root


def start_tk_gui(root):
    try:
        root.mainloop()
    except Exception as e:
        messagebox.showinfo(title='mtxgui info', message=str(e))
