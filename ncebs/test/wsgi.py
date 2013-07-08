import eventlet
from eventlet import wsgi
import webob
import webob.dec
'''
def hello_world(env, start_response):
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    request = webob.request.BaseRequest(env)
    print request.method
    return ['Hello, world!\r\n']

wsgi.server(eventlet.listen(('', 80)), hello_world)
'''

@webob.dec.wsgify
def hello_wsgify(ccc):
    print ccc
    return webob.Response('hey there')

class route(object):
    
    @classmethod
    def factory(cls):
        print 'factory'
        return cls()
    
    @webob.dec.wsgify
    def __call__(self,req):
        print '1111'
        return cc.notcall(req)

    @webob.dec.wsgify
    def notcall(self,req):
        cc = resource()
        print 'not call'
        cc.notcall(req)

class resource(object):

    @webob.dec.wsgify
    def notcall(self,req):
        print 'resource not call'

class API(route):
    def aa(self):
        pass
    
#API.factory().notcall('aa')

wsgi.server(eventlet.listen(('', 80)), API.factory().notcall('aa'))
