'''
Created on 2013-2-26

@author: zhangbin
'''
import os
import re
from subprocess import Popen, PIPE

from util.options import options, define

define('--nginx_bin_path', name='nginx_bin_path', type='string')

class NginxController(object):
    '''
    classdocs
    '''


    def __init__(self, DomainName):
        '''
        Constructor
        '''
        self.DomainName = DomainName
    
    def _TestConf(self):
        
        f = Popen((options.nginx_bin_path+'nginx', '-t'), stderr=PIPE).stderr
        err = f.read()
        regex = re.compile('test is successful')
        ret = re.search(regex, err)
        if ret :
            return True
        else:
            return False
        
    def _ChangeConf(self):
        os.rename(options.nginx_conf_path+self.DomainName+'.conf',
                    options.nginx_conf_path+self.DomainName+'.bak')
        os.rename(options.nginx_conf_path+self.DomainName+'-new.conf',
                    options.nginx_conf_path+self.DomainName+'.conf')
        
    def _ChangeBackConf(self):
        os.remove(options.nginx_conf_path+self.DomainName+'.conf')
        os.rename(options.nginx_conf_path+self.DomainName+'.bak',
                    options.nginx_conf_path+self.DomainName+'.conf')
        
    def RestartNginx(self):
        
        if self._TestConf():
            self._ChangeConf()
        else:
            self._ChangeBackConf()
