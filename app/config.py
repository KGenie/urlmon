import os, app_globals
from helpers import HtmlHelper
from beaker.middleware import SessionMiddleware
from routes import Mapper
from routes.middleware import RoutesMiddleware
from jinja2 import Environment, FileSystemLoader
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from wsgi.app import WebMonitorApp
from wsgi.auth import AuthMiddleware
from wsgi.controller import ControllerMiddleware
from wsgi.request import RequestMiddleware
from wsgi.injection import InjectionMiddleware
from wsgi.http_method import HTTPMethodMiddleware


def make_routes():
    """
    Creates, configure and return the Mapper object.

    This object will be used by the RoutesMiddleware to help in dispatching
    requests to controllers/actions.
    """

    map = Mapper()
    map.directory = os.path.join(app_globals.APP_ROOT, 'controllers')
    map.always_scan = True
    map.minimization = False
    map.explicit = False

    map.connect('/', controller='home', action='main')

    map.connect('/{controller}', action='index')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map

def make_beaker_options():
    return {
            'beaker.session.type': 'memory',
            'beaker.session.auto': True,
            'beaker.session.key': 'webmon',
            'beaker.session.secret': 'webmonsecret'
            }


def make_jinja_environment():
    ret = Environment(loader=FileSystemLoader('./views'))
    ret.globals['h'] = HtmlHelper()
    return ret


def make_auth_options():
    return {
            'required': True, 
            'allow': ('*',), 
            'deny':(),
            'login_controller': 'home',
            'login_action': 'main'
            }


def make_app():
    app_globals.JINJA_ENV = make_jinja_environment()

    app = WebMonitorApp()
    app = InjectionMiddleware(app)
    app = AuthMiddleware(app, **make_auth_options())
    app = RequestMiddleware(app)
    app = HTTPMethodMiddleware(app)
    app = ControllerMiddleware(app)
    app = DispatcherMiddleware(app)
    # All the app's specific middlewares must stay before the
    # dispatcher middleware


    app = RoutesMiddleware(app, make_routes())
    app = SessionMiddleware(app, make_beaker_options())
    path = os.path.join(app_globals.APP_ROOT, 'static')
    app = Cascade([StaticURLParser(path), app])

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

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response)
        return response(environ, start_response)
