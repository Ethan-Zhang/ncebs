'''
Created on 2013-3-4

@author: zhangbin
'''
import datetime
import json
import re

import webob

from common import wsgi
from NginxConfEditor import DomainEditor
from NginxController import NginxController
from db.base import DBBase

class DomainsController(DBBase):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        super(DomainsController, self).__init__()
    
    def index(self, domain, req):
        print req
    
    def create(self, req, domain, name, ip, port):

        editor = DomainEditor(domain)
        editor.addDNS(name, ip, port)
        self.db.dns_add(domain, name, ip, port)
        
    def delete(self, req, domain, name):
        editor = DomainEditor(domain)
        editor.delDNS(name)

class RequestDeserializer(wsgi.JSONRequestDeserializer):
    
    def __init__(self):
        super(RequestDeserializer, self).__init__()
    
    def _get_request_body(self, request):
        output = super(RequestDeserializer, self).default(request)
        print output
        if not 'body' in output:
            msg = 'Body expected in request.'
            raise webob.exc.HTTPBadRequest(msg)
        print output
        return output['body']
    
    def create(self, request):
        body = self._get_request_body(request)
        ip = body.pop('ip', None)
        port = body.pop('port', None)
        
        return dict(ip=ip, port=port)
class ResponseSerializer(wsgi.JSONResponseSerializer):

    def __init__(self):
        super(ResponseSerializer, self).__init__()

    def create(self, response):
        response.status_int = 201

def create_resource():
    '''Domains resource factory method'''
    
    deserializer = RequestDeserializer()
    serializer = ResponseSerializer()
    controller = DomainsController()
    return wsgi.Resource(controller, deserializer, serializer)
