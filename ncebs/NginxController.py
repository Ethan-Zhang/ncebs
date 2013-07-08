'''
Created on 2013-2-26

@author: zhangbin
'''
import os
import re
from subprocess import Popen, PIPE
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
        
        f = Popen(('/usr/local/nginx/sbin/nginx', '-t'), stderr=PIPE).stderr
        err = f.read()
        regex = re.compile('test is successful')
        ret = re.search(regex, err)
        if ret :
            return True
        else:
            return False
        
    def _ChangeConf(self):
        os.rename('/usr/local/nginx/conf/conf.d/'+self.DomainName+'.conf', '/usr/local/nginx/conf/conf.d/'+self.DomainName+'.bak')
        os.rename('/usr/local/nginx/conf/conf.d/'+self.DomainName+'-new.conf', '/usr/local/nginx/conf/conf.d/'+self.DomainName+'.conf')
        
    def _ChangeBackConf(self):
        os.remove('/usr/local/nginx/conf/conf.d/'+self.DomainName+'.conf')
        os.rename('/usr/local/nginx/conf/conf.d/'+self.DomainName+'.bak', '/usr/local/nginx/conf/conf.d/'+self.DomainName+'.conf')
        
    def RestartNginx(self):
        
        if self._TestConf():
            self._ChangeConf()
        else:
            self._ChangeBackConf()
