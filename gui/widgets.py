# coding: utf-8
'''collection of the widgets that are used in the gui'''
import os
import sys
from functools import partial


from Tkinter import Label, Button , Menu, PhotoImage, Frame, Canvas, Scrollbar

# remember the image folder
_imagepath = os.path.join(os.path.split(os.path.dirname(__file__))[0],'img')

# --------------------------------- Labels -------------------------------------

class SlotLabel(Label):
    '''baseclass for the label widgets '''
    def __init__(self,parent, slot):

        self._defaultcolor = parent.cget('bg')
        self._slot = slot
        self._background = self._defaultcolor
        self._text = ''
        self._icon = PhotoImage(file='%s/%s'%(_imagepath,'storage.gif'))
        Label.__init__(self,parent,
                            justify = 'left',
                            anchor= 'w',
                            image = self._icon,
                            text = self._text,
                            bg = self._background,
                            compound = 'left')
        self.grid(padx=2,pady=2,stick='ew')
        self.master.grid_columnconfigure(0,minsize=300)
        self.grid_propagate(0)
        self.bind("<Button-3>",self.onRightClick)
        self.check_slot()

    @property
    def icon(self):
        '''return the gif displayed with the label'''
        return self._icon

    @icon.setter
    def icon(self, value):
        '''set the gif displayed with the label '''
        self._icon = None
        self._icon = PhotoImage(file='%s/%s'%(_imagepath,value))

    @property
    def slot(self):
        '''return the slot from the media changer device that should be
           controled'''
        return self._slot

    @property
    def text(self):
        '''return the text that is displayed with the label '''
        return self._text

    @text.setter
    def text(self, value):
        '''set the text that is displayed on the label  '''
        self._text = value

    @property
    def background(self):
        '''return the color for the label background'''
        return self._background

    @background.setter
    def background(self, value):
        '''set the color for the label background'''
        self._background = value

    @classmethod
    def onRightClick(cls, event):
        '''handle the right click event '''
        print 'if you see this you did it wrong !!!'

    @classmethod
    def updated(cls):
        print 'if you see this you did it wrong !!!'

    @classmethod
    def check_slot(self):
        print 'if you see this you did it wrong !!!'

    @classmethod
    def menu_action(self,slot):
        print 'if you see this you did it wrong !!!'

class StorageLabel(SlotLabel):
    '''class for the storage label '''
    def __init__(self, parent, slot):
        if type(slot).__name__ != 'StorageSlot':
            self.destroy()
        else:
            SlotLabel.__init__(self,parent, slot)
            if self.slot.status == 'Empty':
                self.text = u'%s - %s' % (self.slot.slot,self.slot.status)
                self.background = 'red'
            elif self.slot.status == 'Full ':
                self.text = u'%s - %s' % (self.slot.slot,self.slot.volumetag)
                self.background = 'green'
            #self.check_slot()

    def onRightClick(self, event):
        if self.slot.status == 'Full ':
            popup = Menu(self,tearoff=0)
            popup.add_command(label= u'load',
                        command=partial(self.menu_action, self.slot.slot))
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup.grab_release()
                self.updated()

    def menu_action(self, slot):
        self.slot.device.load(slot)
        #TODO: this cant be the final solution
        self.master.master.master.master.statusbar.config(
                                            text = self.slot.device.last_msg)

    def updated(self):
        if self.slot.status == 'Empty':
            self.background = 'red'
            self.text = u'%s - %s' % (self.slot.slot,self.slot.status)
        elif self.slot.status == 'Full ':
            self.background = 'green'
            self.text = u'%s - %s' % (self.slot.slot,self.slot.volumetag)
        self.config(text=self.text,bg=self.background,image=self.icon)
        self.update_idletasks()

    def check_slot(self):
        self.updated()
        # its not a good idea but it will update the gui without a refesh button
        # lets do it after 5 min
        self.after(500,self.check_slot)

class DataLabel(SlotLabel):
    '''class for the data label '''
    def __init__(self, parent, slot):
        if type(slot).__name__ != 'DataSlot':
            self.destroy()
        else:
            SlotLabel.__init__(self,parent, slot)
            if self.slot.status == 'Empty':
                self.text = self.slot.status
                self.background = self._defaultcolor
            elif self.slot.status == 'Full ':
                self.text = self.slot.status
                self.background = 'orange'

    def onRightClick(self, event):
        if self.slot.status != 'Empty':
            popup = Menu(self,tearoff=0)
            unloadmenu = Menu(self, tearoff = 0)
            for slot in self.slot.device.storage_slots:
                if slot.status == 'Empty':
                    unloadmenu.add_command(label= u'storage slot %s' % slot.slot,
                        command=partial(self.menu_action, slot.slot))
            popup.add_cascade(label='unload',menu =unloadmenu)
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup.grab_release()
                self.updated()

    def menu_action(self, slot):
        self.slot.device.unload(slot)
        #TODO: this cant be the final solution
        self.master.master.master.statusbar.config(
                                            text = self.slot.device.last_msg)

    def updated(self):
        if type(self.slot.status).__name__ == 'tuple':
            self.slot.status = self.slot.status[0]
        if self.slot.status == 'Empty':
            self.background = self._defaultcolor
            self.text = self.slot.status
        elif self.slot.status.find('Full ') != -1:
            self.background = 'orange'
            self.text = self.slot.status
        self.config(text=self.text,bg=self.background,image=self.icon)
        self.update_idletasks()

    def check_slot(self):
        self.updated()
        # its not a good idea but it will update the gui without a refesh button
        # lets do it after 5 min
        self.after(500,self.check_slot)

#-------------------------------- Buttons --------------------------------------

class MediumChangerButton(Button):

    def __init__(self, parent, device,row):
        self._defaultcolor = parent.cget('bg')
        self._device = device
        self._text = device.device
        self._icon = PhotoImage(file='%s/%s'%(_imagepath,'mc.gif'))
        Button.__init__(self, master=parent, image=self._icon,
                        text=self._text, compound='left')
        self.grid(padx=10,pady=10, column = 0, stick='ew')
        self.bind("<Button-1>",self.onClick)
        self.master.grid_columnconfigure(0,minsize=280)

    @property
    def device(self):
        return self._device

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = None
        self._icon = PhotoImage(file='%s/%s'%(_imagepath,value))

    @property
    def text(self):
        return self._text

    def onClick(self, event):
        self.master.master.master.dataframe = DataFrame(
                                self.master.master.master,event.widget.device)
        self.master.master.master.storageframe= StorageFrame(
                                self.master.master.master,event.widget.device)
        #reset the bg of all mediachanger buttons
        for mediachanger in self.master.master.widgets:
            mediachanger.config(bg=self._defaultcolor)
        #set the bg of the clicked button
        self.config(bg='lightgreen')

#------------------------------ Frames -----------------------------------------

class ScrollFrame(Frame):

    def __init__(self, parent, medium_changers=None,device=None):
        Frame.__init__(self, master=parent)
        # init all the stuff we need later on
        self._widgets = None
        self._medium_changers = medium_changers
        self._device = device
        # trick part, get this damn thing scrolling in the right place
        self.grid(stick='nsew')
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.config(height= 380, width= 300)
        self.grid_propagate(0)
        # with a little help, preparing the scrollbar. The final setup happens
        # in the special Slot Class
        self._sbar = AutoScrollbar(self)
        self._sbar.grid(row=0,column=1,stick='ns')
        self._canv = Canvas(self, yscrollcommand=self._sbar.set)
        self._canv.grid(row=0,column=0,stick='nswe')
        self._sbar.config(command=self._canv.yview)
        self.createWidgets()

    @property
    def device(self):
        return self._device

    @property
    def canv(self):
        return self._canv

    @property
    def sbar(self):
        return self._sbar

    @property
    def mediumchangers(self):
        return self._medium_changers

    @property
    def widgets(self):
        return self._widgets

    @widgets.setter
    def widgets(self, value):
        self._widgets = value

    @classmethod
    def createWidgets(cls):
        print 'if you see this you did it wrong !!!'

class ChangerFrame(ScrollFrame):

    def __init__(self, parent ,medium_changers):
        ScrollFrame.__init__(self,parent,medium_changers=medium_changers)
        self.grid(row=0,column=0)

    def createWidgets(self):
        '''creating all the widgets in the main window'''
        if self.mediumchangers:
            # init the buttons for the medium
            counter = 0
            tmp = []
            for mc in self.mediumchangers:
                b = MediumChangerButton(self.canv,mc,counter)
                tmp.append(b)
                b = None
                counter +=1
            self.widgets = tmp

class StorageFrame(ScrollFrame):

    def __init__(self, parent, device):
        ScrollFrame.__init__(self,parent,device=device)
        self.grid(row=0, column=2)

    def createWidgets(self):

        if self.widgets:
            for label in self.widgets:
                label.update()
        else:
            labels =[]
            f = Frame(self.canv)
            f.rowconfigure(0, weight=1)
            f.columnconfigure(0, weight=1)
            for slot in self.device.storage_slots:
                label = StorageLabel(f,slot)
                labels.append(label)

            self.canv.create_window(0, 0, anchor='nw', window=f)
            f.update_idletasks()
            self.canv.config(scrollregion=self.canv.bbox("all"))
            self.widgets = labels

class DataFrame(ScrollFrame):

    def __init__(self, parent, device):
        ScrollFrame.__init__(self,parent,device=device)
        self.grid(row=0,column=1)

    def createWidgets(self):
        if self.widgets:
            for label in self.widgets:
                label.update()
        else:
            labels =[]
            for slot in self.device.data_slots:
                label = DataLabel(self.canv,slot)
                labels.append(label)
            self.widgets = labels

# ----------------------- Scrollbars -------------------------------------------

class AutoScrollbar(Scrollbar):
    ''' Autoscrollbar by Fredrik Lundh '''
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
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"


class StatusBar(Label):

    def __init__(self,parent):
        Label.__init__(self,parent,text='',relief='sunken', anchor='w')
        parent.master.stb= self
        self.grid(column=0, columnspan=4, sticky='ew')
        self._text =''

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.config(text= value)