'''
Created on 2013-4-1

@author: zhangbin
'''

import logging
import traceback

def setup(product_name):
    try:
        logging.basicConfig(filename='/home/zhangbin/ncebs/log/'+product_name ,level=logging.DEBUG)
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
    
