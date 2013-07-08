'''
Created on 2013-3-4

@author: zhangbin
'''
import json
import errno
import os
import signal
import sys

import routes
import routes.middleware
import eventlet
from eventlet.green import socket, ssl
import eventlet.greenio
import eventlet.wsgi
import webob
import webob.dec
import common.log

class Server(object):
    '''Server class to manage multiple WSGI sockets and applications.'''
    
    def __init__(self, threads=1000):
        self.threads = threads
        self.children = []
        self.running = True
        
    def start(self, application, default_port):
        """
        Run a WSGI server with the given application.
        
        :param application: The application to be run in the WSGI server
        :param default_port: Port to bind to
        """
        def kill_children(*args):
            """kills the entire process group."""
            self.logger.info('SIGTERM or SIGINT received')
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            self.running = False
            os.killpg(0, signal.SIGTERM)
        def hup(*args):
            """
            Shuts down the server, but allows running requests to complete
            """
            self.logger.info('SIGHUP received')
            signal.signal(signal.SIGHUP, signal.SIG_IGN)
            self.running = False
        self.application = application
        self.sock = eventlet.listen(('',80))
        
        self.logger = common.log.getLogger('eventlet.wsgi.server')
        
        workers = 1
        
        self.logger.info('Starting %d workers' % workers)
        signal.signal(signal.SIGTERM, kill_children)
        signal.signal(signal.SIGTERM, kill_children)
        signal.signal(signal.SIGHUP, hup)
        while len(self.children) < workers:
            self.run_child()
    
    def create_pool(self):
        eventlet.patcher.monkey_patch(all=False, socket=True)
        return eventlet.GreenPool(size=self.threads)
    
    def wait_on_children(self):
        while self.running:
            try:
                pid, status = os.wait()
                if os.WIFEXITED(status) or os.WIFSGNALED(status):
                    self.logger.info('Removing dead child %s' % pid)
                    self.children.remove(pid)
                    if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
                        self.logger.error('Not respawning child %d, cannot '
                                          'recover from termination' % pid)
                        if not self.children:
                            self.logger.info('All workers have terminated. Exiting')
                            self.running = False
                    else:
                        self.run_child()
            except OSError, err:
                if err.errno not in (errno.EINTR, errno.ECHILD):
                    raise
            except KeyboardInterrupt:
                self.logger.info('Caught keyboard interrupt. Exiting.')
                break
        eventlet.greenio.shutdown_safe(self.sock)
        self.sock.close()
        self.logger.debug('Exited')
        
    def wait(self):
        """Wait until all servers have completed running."""
        try:
            if self.children:
                self.wait_on_children()
            else:
                self.pool.waitall()
        except KeyboardInterrupt:
            pass
                        
    def run_child(self):
        pid = os.fork()
        if pid == 0:
            signal.signal(signal.SIGHUP, signal.SIG_DFL)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            # ignore the interrupt signal to avoid a race whereby
            # a child worker receives the signal before the parent
            # and is respawned unneccessarily as a result
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            self.run_server()
            self.logger.info('Child %d exiting normally' % os.getpid())
            
            sys.exit(0)
        else:
            self.logger.info('Started child %s' %pid)
            self.children.append(pid)
            
    def run_server(self):
        '''Run a WSGI server.'''
        eventlet.wsgi.HttpProtocol.default_request_version = "HTTP/1.0"
        try:
            eventlet.hubs.use_hub('poll')
        except Exception:
            raise
        self.pool = self.create_pool()
        try:
            eventlet.wsgi.server(self.sock,
                                 self.application,
                                 log=common.log.WritableLogger(self.logger),
                                 custom_pool=self.pool)
        except socket.error, err:
            if err[0] != errno.EINVAL:
                raise
        self.pool.waitall()
        
class Router(object):
    """
    WSGI middleware that maps incoming requests to WSGI apps.
    """
    
    def __init__(self, mapper):
        """
        Create a router for the given routes.Mapper
        
        Each route in 'mapper' must specify a 'controller', which is a
        WSGI app to call. You'll probably want to specify an 'action' as
        well and have your controller be a wsgi.Controller, who will route
        the request to the action method.
        
        Examples:
          mapper = routes.Mapper()
          sc = ServerController()
          
          # Explicit mapping of one route to a controller+action
          mapper.connect(None, "/svrlist", controller=sc, action="list")
          
          # Actions are all implicitly defined
          mapper.resource("server", "servers", controller=sc)
          
          # Pointing to an arbitrary WSGI app.  You can specify the
          # {path_info:.*} parameter so the target app can be handed just that
          # section of the URL.
          mapper.connect(None, "/v1.0/{path_info:.*}", controller=BlogApp())
        """
        
        self.map = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.map)

        
    @classmethod
    def factory(cls, global_conf, **local_conf):

        return cls(routes.Mapper())
    
    @webob.dec.wsgify
    def __call__(self, req):
        """
        Route the incoming request to a controller based on self.map.
        If no match, return a 404
        """
        return self._router
    
    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app

    
    
class JSONRequestDeserializer(object):
    def has_body(self, request):
        """
        Returns whether a Webob.Request object will possess an entity body.
        
        :param request: Webob.Request object
        """
        if 'transfer-encoding' in request.headers:
             return True
        elif request.content_length > 0:
             return True
         
        return False
    
    def from_json(self, datastring):
        try:
            return json.loads(datastring)
        except ValueError:
            msg = 'Malformed JSON in request body.'
            raise webob.exc.HTTPBadRequest(msg)
        
    def default(self, request):
        if self.has_body(request):
            return {'body': self.from_json(request.body)}
        else:
            return {}
        
class JSONResponseSerializer(object):
    
    def to_json(self, data):
        def sanitizer(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            return obj
        
        return json.dumps(data, default=sanitizer)
    
    def default(self, response, result):
        response.content_type = 'application/json'
        response.body = self.to_json(result)
        
        
class Resource(object):
    """
    WSGI app that handles (de)serialization and controller dispatch.

    Reads routing information supplied by RoutesMiddleware and calls
    the requested action method upon its deserializer, controller,
    and serializer. Those three objects may implement any of the basic
    controller action methods (create, update, show, index, delete)
    along with any that may be specified in the api router. A 'default'
    method may also be implemented to be used in place of any
    non-implemented actions. Deserializer methods must accept a request
    argument and return a dictionary. Controller methods must accept a
    request argument. Additionally, they must also accept keyword
    arguments that represent the keys returned by the Deserializer. They
    may raise a webob.exc exception or return a dict, which will be
    serialized by requested content type.
    """    
    def __init__(self, controller, deserializer=None, serializer=None):
        """
        :param controller: object that implement methods created by routes lib
        :param deserializer: object that supports webob request deserialization
                             through controller-like actions
        :param serializer: object that supports webob response serialization
                           through controller-like actions
        """        
        self.controller = controller
        self.serializer = serializer or JSONResponseSerializer()
        self.deserializer = deserializer or JSONRequestDeserializer()
        
    @webob.dec.wsgify
    def __call__(self, request):
        """WSGI method that controls (de)serialization and method dispatch."""

        action_args = self.get_action_args(request.environ)
        action = action_args.pop('action', None)

        deserialized_request = self.dispatch(self.deserializer,
                                             action, request)
        action_args.update(deserialized_request)

        action_result = self.dispatch(self.controller, action,
                                      request, **action_args)
        
        try:
            response = webob.Response(request=request)
            self.dispatch(self.serializer, action, response, action_result)
            return response
        
        except Exception:
            return action_result
        
    def dispatch(self, obj, action, *args, **kwargs):
        """Find action-specific method on self and call it."""
        try:
            method = getattr(obj, action)
        except AttributeError:
            method = getattr(obj, 'default')
            
        return method(*args, **kwargs)
    
    def get_action_args(self, request_environment):
        """Parse dictionary created by routes library."""
        try:
            args = request_environment['wsgiorg.routing_args'][1].copy()
        except Exception:
            return {}
        
        try:
            del args['controller']
        except KeyError:
            pass
        
        try:
            del args['format']
        except KeyError:
            pass
        
        return args

        
        