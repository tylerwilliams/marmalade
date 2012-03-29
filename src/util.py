#!/usr/bin/env python
# encoding: utf-8

import urllib
import urllib2
import config
import logging
import socket
import time
import traceback

try:
    import simplejson as json    
except ImportError:
    import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

headers = [('User-Agent', '%s %s' % (config.__version__, config.USER_AGENT))]

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
        if code in [200, 400, 401, 403, 500]:
            return response
        else:
            urllib2.HTTPErrorProcessor.http_response(self, request, response)

opener = urllib2.build_opener(MyBaseHandler(), MyErrorProcessor())
opener.addheaders = headers

def get_successful_response(f_obj):    
    if hasattr(f_obj,'headers'):
        headers = f_obj.headers
    else:
        headers = {'Headers':'No Headers'}
    raw_json = f_obj.read()
    try:
        response_dict = json.loads(raw_json)
        return response_dict
    except ValueError:
        logger.debug(traceback.format_exc())
        raise Exception("Unknown error.",headers)


def callm(method, param_dict, POST=False, socket_timeout=None, data=None):
    """
    Call the api! 
    Param_dict is a *regular* *python* *dictionary* so if you want to have multi-valued params
    put them in a list.
    
    ** note, if we require 2.6, we can get rid of this timeout munging.
    """
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
        url = 'http://%s/%s/%s/%s' % (config.API_HOST, config.API_SELECTOR, 
                                    config.API_VERSION, method)
        
        if data is None:
            data = ''
        data = urllib.urlencode(data)
        data = "&".join([data, params])

        f = opener.open(url, data=data)
    else:
        """
        just a normal GET call
        """
        url = 'http://%s/%s?%s' % (config.API_HOST, method, params)

        f = opener.open(url)
            
    socket.setdefaulttimeout(orig_timeout)
    
    # try/except
    response_dict = get_successful_response(f)
    return response_dict

def fix(x):
    # we need this to fix up all the dict keys to be strings, not unicode objects
    assert(isinstance(x,dict))
    return dict((str(k), v) for (k,v) in x.iteritems())

