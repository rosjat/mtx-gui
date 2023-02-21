# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2015 The mtx-gui Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later
import logging

from Control.api import check_root
from Control.application import Application

app_logger = logging.getLogger("mtx-gui")
app_logger.setLevel(logging.DEBUG)

if check_root():
    app = Application()
    logging.info("starting mtx-gui")
    app.run()
    logging.info("closing mtx-gui")
else:
    app_logger.warning("please start mtx-gui with superuser privileges")
