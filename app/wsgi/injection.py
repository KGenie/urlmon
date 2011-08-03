import app_globals
from helpers import UrlHelper
from app_components.context import Context

class InjectionMiddleware(object):
    """
    Environment/Controller injection middleware

    This middleware is responsible for instantiating the controller class,
    injecting it with the request object, along with all services that may 
    have request specific dependencies. It will also inject request specific
    variables for use in a jinja template.
    """

    def __init__(self, app):
        self.app = app

    
    def __inject_services(self, controller_instance, request):
        # TODO later this will provide the service with a context object,
        # that will by shared by all services. This should also handle
        # injection of cross-service references.
        controller_class = controller_instance.__class__
        for service_name, service_class in controller_class._services.items():
            setattr(controller_instance, service_name, service_class(None))


    def __inject_template_helpers(self, environ):
        controller = environ['route']['controller']
        action = environ['route']['action']
        ctx = {'u': UrlHelper(controller_name=controller,
                action_name=action)}
        session = environ['beaker.session']
        user = environ['beaker.session'].get('user', None)
        if user:
            ctx['user'] = user
        environ['jinja_context'] = ctx
        environ['jinja_environment'] = app_globals.JINJA_ENV


    def __inject_request(self, controller_instance, request):
        setattr(controller_instance, 'request', request)


    def __inject_session(self, controller_instance, session):
        setattr(controller_instance, 'session', session)


    def __call__(self, environ, start_response):
        controller_class = environ['route']['controller_class']
        controller_instance = controller_class()
        request = environ['request']
        session = environ['beaker.session']
        self.__inject_services(controller_instance, request)
        self.__inject_request(controller_instance, request)
        self.__inject_session(controller_instance, session)
        self.__inject_template_helpers(environ)
        environ['route']['controller_instance'] = controller_instance
        return self.app(environ, start_response)
