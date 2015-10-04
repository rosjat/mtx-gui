# coding: utf-8
from distutils.core import setup

setup(name='mtx_gui',
      version='0.1',
      license='LGPLv2.1',
      author='Markus Rosjat',
      author_email='markus.rosjat@gmail.com',
      description='Small GUI for managing Media changers',
      package_data={'mtx_gui.View.img': ['*.gif'], },
      packages=['mtx_gui',
                'mtx_gui.Model',
                'mtx_gui.View',
                'mtx_gui.View.widgets',
                'mtx_gui.View.img',
                'mtx_gui.Control'], )


