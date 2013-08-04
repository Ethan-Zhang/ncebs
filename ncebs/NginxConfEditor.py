'''
Created on 2013-2-25

@author: zhangbin
'''
import os
import re

from util.config import options, define

define('--nginx_conf_path', name='nginx_conf_path', type='string')

class DomainEditor(object):
    '''
    classdocs
    '''

    def __init__(self, DomainName):
        '''
        Constructor
        '''
        self.DomainName = DomainName
        self.ofd = open(options.nginx_conf_path+DomainName+'.conf', 'r+')
        self.nfd = file(options.nginx_conf_path+DomainName+'-new.conf', 'w+')
        
    def addDNS(self, name, ip, port):
        '''
        '''
        if self.findDNS(name):
            return False

        server = [ '################domain ' + name + ' start################' + os.linesep 
                  +'upstream ' + name + '.' + self.DomainName + '.com {' + os.linesep
                  +'\t\t' + 'server ' + ip + ':' + port + ' weight=1;' + os.linesep
                  +'\t\t}' + os.linesep
                  +'server {' + os.linesep
                  +'\t' + 'listen ' + port + ';' + os.linesep
                  +'\t' + 'server_name ' + name + '.' + self.DomainName + '.com;' + os.linesep
                  +'\t' + 'location / {' + os.linesep
                  +'\t\t' + 'proxy_pass ' + 'http://' + name + '.' + self.DomainName + '.com;' +os.linesep
                  +'\t\t' + 'proxy_set_header X-Forwarded-For $remote_addr;' + os.linesep
                  +'\t\t}' + os.linesep
                  +'\t}' + os.linesep
                  +'################domain ' + name + ' end################' + os.linesep]
        servers = self.ofd.read()
        self.nfd.write(servers)
        self.nfd.writelines(server)
        return True
        
    def delDNS(self, name):
        '''
        '''
        if not self.findDNS(name):
            return False
        servers = self.ofd.read()
        regex = re.compile('^##*domain '+name+' start#*(.*\n)+#*domain '+name+' end#*#$',re.M) 
        editservers = re.sub(regex,'',servers)
        self.nfd.write(editservers)
        return True
        
    def findDNS(self, name):
        '''
        '''
        servers = self.ofd.read()
        regex = re.compile('^##*domain '+name+' start#*(.*\n)+#*domain '+name+' end#*#$',re.M)
        server = re.search(regex, servers)
        if server:
            return True
        else:
            return False

