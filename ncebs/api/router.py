'''
Created on 2013-3-4

@author: zhangbin
'''
from api import domains
from common import wsgi

class API(wsgi.Router):
    '''
    WSGI router for ncebs API requests.
    '''


    def __init__(self, mapper):
        '''
        Constructor
        '''
        domain_resource = domains.create_resource()
        mapper.connect('/domains/{domain}',
                       controller=domain_resource,
                       action='index',
                       conditions={'method': ['GET']})
        
        mapper.connect('/domains/{domain}/{name}',
                       controller=domain_resource,
                       action='create',
                       conditions={'method': ['POST']})
        
        mapper.connect('/domains/{domain}/{name}',
                       controller=domain_resource,
                       action='delete',
                       conditions={'method': ['DELETE']})
        
        super(API, self).__init__(mapper)
