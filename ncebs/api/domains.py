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
    
    def index(self, req):
        print req
    
    def create(self, req, url, ip, port):
        
        def domainparse(url):
            m = re.search('\w+\.\w+$',url)
            domain = '%s' % m.group()
            name = url[ 0 : url.rfind(domain)-1 ]
            return domain, name
        
        domain, name = domainparse(url)
        editor = DomainEditor(domain)
        editor.addDNS(name, ip, port)
        self.db.dns_add(domain, name, ip, port)
        
    def delete(self, req, domain, name):
        editor = DomainEditor(domain)
        editor.delDNS(name)

class RequestDeserializer(wsgi.JSONRequestDeserializer):
    
    def __init__(self):
        pass
    
    def _get_request_body(self, request):
        output = super(RequestDeserializer, self).default(request)
        if not 'body' in output:
            msg = 'Body expected in request.'
            raise webob.exc.HTTPBadRequest(msg)
        return output['body']
    
    def create(self, request):
        body = self._get_request_body(request)
        url = body.pop('url', None)
        ip = body.pop('ip', None)
        port = body.pop('port', None)
        
        return dict(url=url, ip=ip, port=port)
    
def create_resource():
    '''Domains resource factory method'''
    
    deserializer = RequestDeserializer()
    controller = DomainsController()
    return wsgi.Resource(controller, deserializer)
