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
import logging
from mtx_gui.Control.application import Application
from mtx_gui.Control.api import check_root

app_logger = logging.getLogger('mtx-gui')
app_logger.setLevel(logging.DEBUG)

if check_root():
    app = Application()
    logging.info('starting mtx-gui')
    app.run()
    logging.info('closing mtx-gui')
else:
    app_logger.warning('please start mtx-gui with superuser privileges')
