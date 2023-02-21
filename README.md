<!--
SPDX-FileCopyrightText: 2015 The mtx-gui Authors

SPDX-License-Identifier: LGPL-2.1-or-later
-->

# mtx-gui


This will be the "new" version of mtx-gui so it's not fully functional right now.
But as you may noticed it's going in a different direction then the master branch.
It aims to use the python-scsi package (https://github.com/rosjat/python-scsi) but
it will offer a fallback to the mtx tool if python-scsi package is not installed.

## Updates

### 2023-02-21
made some changes to the project and moved the setup to setup.cfg and pyproject.toml
Also added pre-commit-hooks and a github workflow to make use of tools to keep the code
reusable. That said i will try to put in a little work once in a while to get the project
to a state where people could use the dev branch ...

### 2015-11-14
Ok its basically working now, added code for the load and unload of the slots.
It's in a dev stage still but with this codebase it should at least do the things
the old gui have done now. Well except the statusbar but this is going to be implemented
as soon as this version is working "well".


### 2015-11-08
Just some minor changes in the GUI, it start to look a bit nicer now.

### 2015-10-06
the gui can at least be started now, as long as you are doing it as root for the dev access and you should have
a media changer or at least as iscsi target set up with tgt (for example)

### 2015-10-04
since python-scsi now supports python 3 I started to organize the dev branch so I get a nice base for
the next steps to come. MediumChanger is now a pyscsi.SCSIDevice.

I also changed dev_mr to the default branch!

## Getting the sources

The module is hosted at https://github.com/rosjat/mtx-gui

You can use git to checkout the latest version of the source code using:

    $ git clone git@github.com:rosjat/mtx-gui.git

It is also available as a downloadable zip archive from:

master: https://github.com/rosjat/mtx-gui/archive/master.zip

dev:  https://github.com/rosjat/mtx-gui/archive/dev_mr.zip


## Building and installing

Building the module:

    $ python3 setup.py build

Installing the module:

    $ python3 setup.py install

Installing with pip:

    $ pip install .

Using the module:

**Note:** you need to be a superuser to run the GUI

    $ sudo python3 /path_to_mtx_gui
