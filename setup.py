#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name = 'bottle-redis',
    version = '0.2.2',
    url = 'https://github.com/bottlepy/bottle-redis',
    description = 'Redis integration for Bottle.',
    author = 'Sean M. Collins',
    author_email = 'sean@coreitpro.com',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_redis'
    ],
    install_requires = REQUIREMENTS,
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Bottle'
    ],
)

