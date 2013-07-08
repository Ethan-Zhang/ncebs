from NginxConfEditor import *
from NginxController import *

#conf = DomainEditor('hualuyunhai')
#conf.addDNS('test2','10.2.15.333','80')
#conf.delDNS('cloud')

con = NginxController('hualuyunhai')
ret=con.TestConf()
print ret


