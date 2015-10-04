# coding: utf-8
"""collection of the widgets that are used in the View"""
from functools import partial
from tkinter import Label, PhotoImage, Menu
from . import _imagepath


class SlotLabel(Label):
    """baseclass for the label widgets"""
    def __init__(self,parent, slot):

        self._defaultcolor = parent.cget('bg')
        self._slot = slot
        self._background = self._defaultcolor
        self._text = ''
        self._icon = PhotoImage(file='%s/%s'%(_imagepath,'storage.gif'))
        Label.__init__(self,
                       parent,
                       justify='left',
                       anchor='w',
                       image=self._icon,
                       text=self._text,
                       bg=self._background,
                       compound='left')
        self.grid(padx=2,
                  pady=2,
                  stick='ew')
        self.master.grid_columnconfigure(0, minsize=300)
        self.grid_propagate(0)
        self.bind("<Button-3>", self.onRightClick)
        self.check_slot()

    @property
    def icon(self):
        """return the gif displayed with the label"""
        return self._icon

    @icon.setter
    def icon(self, value):
        """set the gif displayed with the label"""
        self._icon = None
        self._icon = PhotoImage(file='%s/%s' % (_imagepath, value))

    @property
    def slot(self):
        """return the slot from the media changer device that should be controled"""
        return self._slot

    @property
    def text(self):
        """return the text that is displayed with the label"""
        return self._text

    @text.setter
    def text(self, value):
        """set the text that is displayed on the label"""
        self._text = value

    @property
    def background(self):
        """return the color for the label background"""
        return self._background

    @background.setter
    def background(self, value):
        """set the color for the label background"""
        self._background = value

    def onRightClick(self, event):
        """handle the right click event"""
        print('if you see this you did it wrong !!!')

    def updated(self):
        print('if you see this you did it wrong !!!')

    def check_slot(self):
        print('if you see this you did it wrong !!!')

    def menu_action(self, slot):
        print('if you see this you did it wrong !!!')


class StorageLabel(SlotLabel):
    """class for the storage label"""
    def __init__(self, parent, slot):
        if type(slot).__name__ != 'StorageSlot':
            self.destroy()
        else:
            SlotLabel.__init__(self,parent, slot)
            if self.slot.status == 'Empty':
                self.text = u'%s - %s' % (self.slot.slot, self.slot.status)
                self.background = 'red'
            elif self.slot.status == 'Full ':
                self.text = u'%s - %s' % (self.slot.slot, self.slot.volumetag)
                self.background = 'green'
            #self.check_slot()

    def onRightClick(self, event):
        if self.slot.status == 'Full ':
            popup = Menu(self,tearoff=0)
            popup.add_command(label=u'load', command=partial(self.menu_action, self.slot.slot))
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup.grab_release()
                self.updated()

    def menu_action(self, slot):
        self.slot.device.load(slot)
        # TODO: this cant be the final solution
        self.master.master.master.master.statusbar.config(text=self.slot.device.last_msg)

    def updated(self):
        if self.slot.status == 'Empty':
            self.background = 'red'
            self.text = u'%s - %s' % (self.slot.slot, self.slot.status)
        elif self.slot.status == 'Full ':
            self.background = 'green'
            self.text = u'%s - %s' % (self.slot.slot, self.slot.volumetag)
        self.config(text=self.text,bg=self.background, image=self.icon)
        self.update_idletasks()

    def check_slot(self):
        self.updated()
        # its not a good idea but it will update the View without a refresh button
        # lets do it after 5 min
        self.after(500, self.check_slot)


class DataLabel(SlotLabel):
    """class for the data label"""
    def __init__(self, parent, slot):
        if type(slot).__name__ != 'DataSlot':
            self.destroy()
        else:
            SlotLabel.__init__(self, parent, slot)
            if self.slot.status == 'Empty':
                self.text = self.slot.status
                self.background = self._defaultcolor
            elif self.slot.status == 'Full ':
                self.text = self.slot.status
                self.background = 'orange'

    def onRightClick(self, event):
        if self.slot.status != 'Empty':
            popup = Menu(self,tearoff=0)
            unloadmenu = Menu(self, tearoff=0)
            for slot in self.slot.device.storage_slots:
                if slot.status == 'Empty':
                    unloadmenu.add_command(label=u'storage slot %s' % slot.slot,
                                           command=partial(self.menu_action, slot.slot))
            popup.add_cascade(label='unload', menu=unloadmenu)
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup.grab_release()
                self.updated()

    def menu_action(self, slot):
        self.slot.device.unload(slot)
        # TODO: this cant be the final solution
        self.master.master.master.statusbar.config(text=self.slot.device.last_msg)

    def updated(self):
        if type(self.slot.status).__name__ == 'tuple':
            self.slot.status = self.slot.status[0]
        if self.slot.status == 'Empty':
            self.background = self._defaultcolor
            self.text = self.slot.status
        elif self.slot.status.find('Full ') != -1:
            self.background = 'orange'
            self.text = self.slot.status
        self.config(text=self.text, bg=self.background, image=self.icon)
        self.update_idletasks()

    def check_slot(self):
        self.updated()
        # its not a good idea but it will update the View without a refresh button
        # lets do it after 5 min
        self.after(500, self.check_slot)


class StatusBar(Label):

    def __init__(self, parent):
        Label.__init__(self, parent, text='', relief='sunken', anchor='w')
        parent.master.stb = self
        self.grid(column=0, columnspan=4, sticky='ew')
        self._text = ''

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.config(text=value)
