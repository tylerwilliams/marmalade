#!/usr/bin/env python
# encoding: utf-8
import pkg_resources

try:
    __version__ = pkg_resources.require("marmalade")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0"

API_HOST = 'api.thisismyjam.com'
USER_AGENT = 'marmalade'
TRACE_API_CALLS = False
CALL_TIMEOUT = 10
API_VERSION = 1
