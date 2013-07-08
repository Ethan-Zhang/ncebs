'''
Created on 2013-3-4

@author: zhangbin
'''
import sys
sys.path.append('/var/local/ncebs/ncebs')

from common import log
from common import wsgi
from api import router

if __name__ == '__main__':
    
    log.setup('ncebs')
    server = wsgi.Server()
    server.start(router.API.factory('aa'), default_port=80)
    server.wait()