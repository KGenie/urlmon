import os, sys, glob, app_globals, logging, fork_vars, atexit,\
        app_config
from traceback import format_exc
from helpers import HtmlHelper, UrlHelper
from pipestream import PipeStream
from beaker.middleware import SessionMiddleware
from webob.exc import HTTPNotFound
from routes import Mapper
from routes.middleware import RoutesMiddleware
from jinja2 import Environment, FileSystemLoader
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from util import get_controller_class_name
from database import sqlalch


CONTROLLER_CACHE = None

def make_routes():
    """
    Creates, configure and return the Mapper object.

    This object will be used by the RoutesMiddleware to help in dispatching
    requests to controllers/actions.
    """

    map = Mapper()
    map.directory = os.path.join(app_globals.APP_ROOT, 'controllers')
    map.always_scan = False
    map.minimization = True
    map.explicit = False
    map.connect('/', controller='home', action='main')
    map.connect('/{controller}', action='index')
    map.connect('/{controller}/{action}')
    return map


def make_beaker_options():
    return {
            'beaker.session.type': 'memory',
            'beaker.session.auto': True,
            'beaker.session.key': 'webmon',
            'beaker.session.secret': 'webmonsecret',
            }


def make_jinja_web_environment():
    ret = Environment(loader=FileSystemLoader('./views'))
    ret.globals['h'] = HtmlHelper()
    return ret


def make_auth_options():
    return {'login_controller': 'home',
            'login_action': 'main'}


def ensure_is_decorated(controller_class, default_permissions_decorator):
    decorated_flag_key = '_auth_decorated'
    # apply default access control settings 
    if not hasattr(controller_class, decorated_flag_key):
        default_permissions_decorator(controller_class)
        setattr(controller_class, decorated_flag_key, True)


def make_controllers():
    from wsgi.auth import auth
    """
    Imports all controllers.

    Imports all controllers and returns a dict containing all names/classes.
    """
    ret = {}

    default_permissions_decorator = auth(required=True,allow=('*',),deny=())

    controller_names =  (f.replace('.py','').split('/')[1]\
            for f in glob.glob('controllers/*.py') if\
            '__init__.py' not in f)

    for controller_name in controller_names:
        module_name = 'controllers.%s' % controller_name
        __import__(module_name, globals=globals(),fromlist=[controller_name])
        module = sys.modules[module_name]
        controller_class_name = get_controller_class_name(controller_name)
        if hasattr(module, controller_class_name):
            controller_class = getattr(module, controller_class_name, None)
            ensure_is_decorated(controller_class,
                    default_permissions_decorator)
            ret[controller_name] = controller_class
    return ret


def start_daemon(daemon, parent_pid):
    daemon.start()
    if os.getpid() != parent_pid:
        sys.exit(0)


def stop_daemons():
    from daemons import logger, mailer, webpage, task, cleanup

    daemons = [cleanup.DAEMON, task.DAEMON, mailer.DAEMON, webpage.DAEMON,
            logger.DAEMON]
    for daemon in daemons:
        daemon.stop()

    os.close(fork_vars.LOG_WRITE)



def start_daemons():
    parent_pid = os.getpid()

    from daemons import logger
    start_daemon(logger.DAEMON, parent_pid)
    os.close(fork_vars.LOG_READ)

    from daemons import mailer
    start_daemon(mailer.DAEMON, parent_pid)

    from daemons import webpage
    start_daemon(webpage.DAEMON, parent_pid)

    from daemons import task
    start_daemon(task.DAEMON, parent_pid)

    from daemons import cleanup
    start_daemon(cleanup.DAEMON, parent_pid)

    

def setup_logging():
    print 'Temp directory is %s' % fork_vars.LOG_DIR

    readfd, writefd = os.pipe()
    fork_vars.LOG_READ = readfd
    fork_vars.LOG_WRITE = writefd

    stream = PipeStream(writefd, read=False, write=True)
    formatter =\
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    for k,v in app_config.LEVELS.items():
        handler = logging.StreamHandler(stream)
        handler.setFormatter(formatter)
        logging.getLogger(k).addHandler(handler)
        logging.getLogger(k).setLevel(v)
        logging.getLogger(k).propagate = 0



def make_app():
    setup_logging() # logging before daemons so we will share logger setup
    start_daemons() # this is where we fork

    # Do these imports here to avoid having modules loaded before forking
    from wsgi.app import WebMonitorApp
    from wsgi.auth import AuthMiddleware
    from wsgi.controller import ControllerMiddleware
    from wsgi.request import RequestMiddleware
    from wsgi.injection import InjectionMiddleware
    from wsgi.http_method import HTTPMethodMiddleware

    
    atexit.register(stop_daemons)
    app_globals.JINJA_ENV = make_jinja_web_environment()
    global CONTROLLER_CACHE
    CONTROLLER_CACHE = make_controllers()
  
    app = WebMonitorApp()
    app = InjectionMiddleware(app)
    app = AuthMiddleware(app, **make_auth_options())
    app = RequestMiddleware(app)
    app = HTTPMethodMiddleware(app)
    app = ControllerMiddleware(app, CONTROLLER_CACHE)
    app = DispatcherMiddleware(app)
    # All the app's specific middlewares must stay before the
    # dispatcher middleware


    app = RoutesMiddleware(app, make_routes())
    app = SessionMiddleware(app, make_beaker_options())
#    path = os.path.join(app_globals.APP_ROOT, 'static')
    app = Cascade([app, StaticURLParser(app_globals.APP_ROOT)])

    

    return app




class DispatcherMiddleware(object):
    """
    Response Dispatcher Middleware.

    This middleware expects it's app to return another app object, which
    will encapsulate the response. This response object must be responsible
    for actually invoking the 'start_response' callback.
    """

    def __init__(self, app):
        self.app = app
        logger = logging.getLogger('dispatcher')
        self.debug = logger.debug
        self.warn = logger.warn
        self.error = logger.error
        self.info = logger.info


    def __call__(self, environ, start_response):
        s = sqlalch.Session()
        response = None
        try:
            response = self.app(environ, start_response)
        except Exception, e:
            s.rollback()
            self.error('Exception happened while dispatching the request %s'\
                    % format_exc(e))
        else:
            if response:
                s.commit()
            else:
                s.rollback()
        finally:
            s.close()

        if not response:
            return HTTPNotFound()(environ, start_response)

        return response(environ, start_response)
