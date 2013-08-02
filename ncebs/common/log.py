'''
Created on 2013-4-1

@author: zhangbin
'''

import os
import logging
import logging.handlers
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
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s', '')
        _console=logging.StreamHandler();
        _file=logging.FileHandler(log_dir+'/'+product_name+'.log')
        _file.setFormatter(formatter)
        _console.setFormatter(formatter)
        logger.addHandler(_console)
        logger.addHandler(_file)
    except Exception:
        traceback.print_exc()
        raise

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

LOG = logging.getLogger()    
