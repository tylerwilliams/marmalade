#!/usr/bin/env python
# encoding: utf-8

import gzip
import time
import socket
import urllib
import urllib2
import logging
import StringIO
import threading

try:
    import simplejson as json
except ImportError:
    import json

import config
import timj_exceptions

logging.basicConfig(level=logging.INFO, format="%(name)s - %(message)s")
logger = logging.getLogger("marmalade")
l = threading.local()
l.opener = None

headers = [
    ('User-Agent', '%s %s' % (config.__version__, config.USER_AGENT)),
    ('Accept-encoding', 'gzip'),
]

class MyBaseHandler(urllib2.BaseHandler):
    def default_open(self, request):
        if config.TRACE_API_CALLS:
            logger.info("%s" % (request.get_full_url(),))
        request.start_time = time.time()
        return None

class MyErrorProcessor(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        code = response.code
        if config.TRACE_API_CALLS:
            logger.info("took %2.2fs: (%i)" % (time.time()-request.start_time,code))
        if code in [200, 400, 401, 403, 404, 500]:
            return response
        else:
            urllib2.HTTPErrorProcessor.http_response(self, request, response)

def decode_response(f_obj):
    if f_obj.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(f_obj.read())
        f_obj = gzip.GzipFile(fileobj=buf)
    return f_obj

def get_successful_response(f_obj, response_code, response_headers):
    response_headers = response_headers or {'Headers':'No Headers'}
    raw_json = f_obj.read()
    try:
        response_dict = json.loads(raw_json)
        if 400 <= response_code < 500:
            raise timj_exceptions.TIMJAPIError(response_dict['message'] or response_dict['text'], response_headers)
        return response_dict
    except ValueError:
        logger.exception()
        raise timj_exceptions.TIMJAPIError("Unknown error.", response_headers)

def callm(method, param_dict, POST=False, socket_timeout=None, data=None):
    """
    Call the api!
    Param_dict is a *regular* *python* *dictionary* so if you want to have multi-valued params
    put them in a list.

    ** note, if we require 2.6, we can get rid of this timeout munging.
    """
    global l
    if not l.opener:
        opener = urllib2.build_opener(MyBaseHandler(), MyErrorProcessor())
        opener.addheaders = headers
        l.opener = opener

    param_dict['key'] = config.TIMJ_API_KEY
    param_list = []
    if not socket_timeout:
        socket_timeout = config.CALL_TIMEOUT

    for key,val in param_dict.iteritems():
        if isinstance(val, list):
            param_list.extend( [(key,subval) for subval in val] )
        elif val is not None:
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            param_list.append( (key,val) )

    params = urllib.urlencode(param_list)

    orig_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(socket_timeout)

    if(POST):
        """
        this is a normal POST call
        """
        url = 'http://%s/%s/%s' % (config.API_HOST, config.API_VERSION, method)

        if data is None:
            data = ''
        data = urllib.urlencode(data)
        data = "&".join([data, params])

        f = l.opener.open(url, data=data)
    else:
        """
        just a normal GET call
        """
        url = 'http://%s/%s/%s?%s' % (config.API_HOST, config.API_VERSION, method, params)

        f = l.opener.open(url)

    socket.setdefaulttimeout(orig_timeout)
    response_code = f.getcode()
    response_headers = dict(f.headers)

    f = decode_response(f)
    response_dict = get_successful_response(f, response_code, response_headers)
    return response_dict

def fix(x):
    # we need this to fix up all the dict keys to be strings, not unicode objects
    assert(isinstance(x,dict))
    return dict((str(k), v) for (k,v) in x.iteritems())

