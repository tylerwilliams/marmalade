#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import warnings
import pkg_resources

try:
    __version__ = pkg_resources.require("marmalade")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0" # no version--maybe pkg is not installed

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

if not TIMJ_API_KEY:
    warnings.warn("TIMJ_API_KEY is not set!")