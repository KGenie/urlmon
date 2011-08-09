"""
Response objects used by the application

The purpose of this module is to provide custom response classes(such as
JinjaResponse) and to provide a layer of indirection into the webob
framework(making easy to replace case it is necessary)
"""
from webob import Response
from webob.exc import _HTTPMove, HTTPNotFound, HTTPForbidden,\
        HTTPMethodNotAllowed, HTTPInternalServerError
from helpers import UrlHelper
from jinja2 import TemplateNotFound


url_helper = UrlHelper()

class JinjaResponse(Response):

    def __init__(self, request, name, controller_name, context, **kwargs):
        super(JinjaResponse, self).__init__(**kwargs)

        jinja_environment = request.environ['jinja_environment']
        jinja_context = request.environ['jinja_context']

        template = None
        first_search_path = controller_name + '/'
        second_search_path = 'shared/'
        try:
            template = jinja_environment.get_template(first_search_path + name)
        except TemplateNotFound:
            template = jinja_environment.get_template(second_search_path + name)

        final_context = jinja_context
        if context: 
            if not isinstance(context, dict):
                context = context.__dict__
            final_context = dict(context.items() + final_context.items())

        self.unicode_body = template.render(**final_context)


class RedirectResponse(_HTTPMove):
    code = 303
    title = 'See other'

    def __init__(self, controller, action, qsargs, **kwargs):
        location = url_helper.action(name=action, controller=controller,
                **qsargs)
        super(RedirectResponse, self).__init__(location=location, **kwargs)


class StaticContentResponse(Response):
    pass

class RedirectToLoginResponse(RedirectResponse):
    code = 303
    title = 'Identify yourself'

    def __init__(self, controller='login', action='sign_in', **kwargs):
        super(RedirectToLoginResponse, self).\
                __init__(controller, action, **kwargs)

class ServerErrorResponse(HTTPInternalServerError):
    pass

class NotFoundResponse(HTTPNotFound):
    pass

class NotAuthorizedResponse(HTTPForbidden):
    pass

class MethodNotAllowedResponse(HTTPMethodNotAllowed):
    pass
