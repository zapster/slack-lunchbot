#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

NAME = 'lunchbot'
VERSION = '0.0.1'
DESCRIPTION = 'Exporting food data from the Mensa IBM mainframe since 2017'
REQUIRES_PYTHON = '>=3.6.0'

REQUIRED = [
    'requests~=2.18.0',
    'slackclient~=1.2.0',
    'beautifulsoup4~=4.6.0',
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['{0:s} = {0:s}.__main__:cli'.format(NAME)],
    }
)
