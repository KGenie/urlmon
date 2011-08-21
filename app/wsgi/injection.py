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
        from services.menu import MenuService
        self.app = app
        self.MenuService = MenuService


        
    def __inject_services(self, controller_instance, request):
        # TODO later this will provide the service with a context object,
        # that will by shared by all services. This should also handle
        # injection of cross-service references.
        controller_class = controller_instance.__class__
        serv_cache = {}
        for service_name, service_class in controller_class._services.items():
            if service_name not in serv_cache:
                serv_cache[service_name] = service_class(request)
            setattr(controller_instance, service_name, serv_cache[service_name])


    def __inject_template_helpers(self, environ, request):
        controller = environ['route']['controller']
        action = environ['route']['action']
        ctx = {'u': UrlHelper(controller_name=controller,
                action_name=action)}
        menu_service = self.MenuService(request)
        sitemap = menu_service.sitemap()
        ctx['sitemap'] = sitemap

        session = environ['beaker.session']
        user = session.get('user', None)
        if user:
            ctx['user'] = user

        flash = None

        flash_success = session.get('flash-success', None)
        if flash_success:
            del session['flash-success']
            flash = {'message': flash_success, 'type': 'success'}
        
        flash_error = session.get('flash-error', None)
        if flash_error:
            del session['flash-error']
            flash = {'message': flash_error, 'type': 'error'}
            
        if flash:
            ctx['flash'] = flash

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
        self.__inject_template_helpers(environ, request)
        environ['route']['controller_instance'] = controller_instance
        return self.app(environ, start_response)
