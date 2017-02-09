#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016-2017 by Sylvain Boily
# SPDX-License-Identifier: GPL-3.0+

from setuptools import setup
from setuptools import find_packages


setup(
    name='XiVO confgend kamailio SIP',
    version='0.0.1',

    description='Driver for connect Wazo and Kamailio',

    packages=find_packages(),

    entry_points={
        'xivo_confgend.asterisk.sip.conf': [
            'kamailio = src.driver:KamailioDriver',
        ],
    }
)
