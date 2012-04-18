#!/usr/bin/env python
# encoding: utf-8

__version__ = "1.1.0"

# $Source$
from sys import version
import os
from setuptools import setup

if version < '2.6':
    requires=['urllib', 'urllib2', 'simplejson']
elif version >= '2.6':
    requires=['urllib', 'urllib2', 'json']
else:
    #unknown version?
    requires=['urllib', 'urllib2']

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='marmalade',
    version=__version__,
    description='Python interface to This Is My Jam API.',
    long_description=read('README.md'),
    author='Tyler Williams',
    author_email='williams.tyler@gmail.com',
    maintainer='Tyler Williams',
    maintainer_email='williams.tyler@gmail.com',
    url='https://github.com/echonest/marmalade',
    download_url='https://github.com/echonest/marmalade',
    package_dir={'marmalade':'marmalade'},
    packages=['marmalade'],
    requires=requires
)
