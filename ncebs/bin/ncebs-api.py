#!/usr/bin/env python

'''
Created on 2013-3-4

@author: zhangbin
'''
import sys
import os
# If ../ncebs/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                        os.pardir,
                                        os.pardir))
if os.path.exists(os.path.join(possible_topdir, '__init__.py')):
        sys.path.insert(0, possible_topdir)


from util import config
from common import log
from common import wsgi
from api import router

if __name__ == '__main__':
    
    config.parse_command_line()
    log.setup('ncebs')
    server = wsgi.Server()
    server.start(router.API.factory('aa'), default_port=9204)
    server.wait()
