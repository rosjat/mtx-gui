# mtx-gui


This will be the "new" version of mtx-gui so it's basically
not functional right now because I just want to store it somewhere
safe. But as you may noticed it's going in a different direction then the
master branch

### Update 2015-10-04
since python-scsi now supports python 3 I started to organize the dev branch so I get a nice base for
the next steps to come. MediumChanger is now a pyscsi.SCSIDevice.

I also changed dev_mr to the default branch!

## License

mtx-gui is distributed under LGPLv2.1
Please see the LICENSE file for the full license text.


## Getting the sources

The module is hosted at https://github.com/rosjat/mtx-gui

You can use git to checkout the latest version of the source code using:

    $ git clone git@github.com:rosjat/mtx-gui.git

It is also available as a downloadable zip archive from:

    https://github.com/rosjat/mtx-gui/archive/master.zip 


## Building and installing

Building the module:

    $ python3 setup.py build
    
Installing the module:

    $ python3 setup.py install

Using the module:

    $ python3 /path_to_mtx_gui
