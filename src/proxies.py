#!/usr/bin/env python
# encoding: utf-8

import util

class ResultList(list):
    def __init__(self, li, start=0, total=0):
        self.extend(li)
        self.start = start
        if total == 0:
            total = len(li)
        self.total = total

class GenericProxy(object):
    def __init__(self):
        self.cache = {}
    
    def get_json_resource(self, resource_name, **kwargs):
        result = util.callm("%s.json" % resource_name, kwargs)
        return result
    
class UserProxy(GenericProxy):
    def __init__(self, name, **kwargs):
        super(UserProxy, self).__init__()
        self.id = name
        kwargs = util.fix(kwargs)
        core_attrs = [] # things you want/need initted at object creation time

        if not all(core_attr in kwargs for core_attr in core_attrs):
            profile = self.get_json_resource(self.id)['person']
            kwargs.update(profile)
        
        self.cache.update(kwargs)
        
    def get_json_user_attribute(self, attribute_name, **kwargs):
        meta_resource_name = "%s/%s" % (self.id, attribute_name)
        return self.get_json_resource(meta_resource_name, **kwargs)
    