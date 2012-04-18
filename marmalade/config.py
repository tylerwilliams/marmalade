#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import pkg_resources

try:
    __version__ = pkg_resources.require("marmalade")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0"

TIMJ_API_KEY = None
API_HOST = 'api.thisismyjam.com'
USER_AGENT = 'marmalade - %s' % __version__
API_VERSION = 1
TRACE_API_CALLS = False
CALL_TIMEOUT = 10

envkeys = ["TIMJ_API_KEY"]
this_module = sys.modules[__name__]
for key in envkeys:
    setattr(this_module, key, os.environ.get(key, None))
