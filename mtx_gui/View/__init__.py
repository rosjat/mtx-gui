# coding: utf-8
'''collection of the widgets that are used in the View'''
import os
import sys
from functools import partial


from Tkinter import Label, Button , Menu, PhotoImage, Frame, Canvas, Scrollbar

# remember the image folder
_imagepath = os.path.join(os.path.split(os.path.dirname(__file__))[0],'img')