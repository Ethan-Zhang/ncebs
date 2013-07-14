'''
Created on 2013-4-1

@author: zhangbin
'''

import os
import logging
import traceback

from util.config import options, define

define('--log-dir', name='logdir', type='string')

def setup(product_name):
    try:
        log_dir = options.logdir
        if not log_dir:
            log_dir = os.path.normpath(os.path.join(__file__, 
                                                    os.pardir, 
                                                    os.pardir, 
                                                    os.pardir,
                                                    'log'))
        logging.basicConfig(filename=log_dir+'/'+product_name+'.log' ,level=logging.DEBUG)
    except Exception:
        traceback.print_exc()
        raise

def getLogger(name='unknown'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
    
class WritableLogger(object):
    '''
    classdocs
    '''


    def __init__(self, logger, level=logging.INFO):
        '''
        Constructor
        '''
        self.logger = logger
        self.level = level
        
    def write(self, msg):
        self.logger.log(self.level, msg)
    
